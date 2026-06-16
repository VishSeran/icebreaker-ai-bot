from typing import Any, Optional
from llama_index.core import Document
from llama_index.core.node_parser import SentenceSplitter
import json
from modules.config import CHUNK_SIZE, CHUNK_OVERLAP, EMBEDDING_MODEL_ID
from logging import Logger
from llama_index.core.storage.storage_context import StorageContext
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import VectorStoreIndex
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
import chromadb

logger = Logger(name="logger")

def split_json_data(profile_json:dict[str,Any])-> list:
    
    try:
        
        profile_json_data = json.dumps(profile_json)
        documents = Document(text=profile_json_data)
        
        splitter = SentenceSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)
        nodes = splitter.get_nodes_from_documents([documents],show_progress=True)
        
        logger.info(f"Created {len(nodes)} of nodes from profile_json data")
        return nodes
    
    except Exception as e:
        logger.error(f"error during creating nodes: {e}")
        print(f"Unknown error: {e}")
        return []
        
    
def create_vector_database(nodes:list) -> Optional[VectorStoreIndex]:
      
    try:
        
        db = chromadb.PersistentClient(path="chroma_db_linkedin")
        chroma_collection = db.get_or_create_collection("linkedin_collection")
        vector_store = ChromaVectorStore(
            chroma_collection=chroma_collection, 
        )
        
        storage_context = StorageContext.from_defaults(
            vector_store=vector_store
        )
        
        embed_model = HuggingFaceEmbedding(
            model=EMBEDDING_MODEL_ID
        )
        index = VectorStoreIndex(
            nodes=nodes,
            embed_model=embed_model,
            storage_context=storage_context
        )
        
        logger.info("Creating vector index and returned")
        return index
    except Exception as e:
        print(f"Unknown error: {e}")
        logger.error("an error while creating vector index")
        return None
    

def verify_verctor_database(index:VectorStoreIndex) -> bool:
    
    try:
        
        vector_store = index.storage_context.vector_store
        node_ids = list(index.index_struct.nodes_dict.keys())
        missing = []
        
        
        for node_id in node_ids:
            vector_embedding = vector_store.get_nodes(node_ids=[node_id])[0].get_embedding()
            
            if vector_embedding is None or len(vector_embedding) == 0:
                logger.warning(f"the node id {node_id} has none embedding")
                missing.append(node_id)
            
            else:
                logger.debug(f"node id: {node_id} has a embedding")
 
        if missing:
            logger.warning("some ids have none or empty embeddings")
            return False
        else:
            logger.debug("all the nodes have proper embedding values")
            return True
        
    except Exception as e:
        print(f"Error verifying embeddings: {e}")
        return False