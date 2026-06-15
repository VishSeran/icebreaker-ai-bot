from typing import Any
from llama_index.core import Document
from llama_index.core.node_parser import SentenceSplitter
import json
from modules.config import CHUNK_SIZE, CHUNK_OVERLAP
from logging import Logger

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
        
    
    