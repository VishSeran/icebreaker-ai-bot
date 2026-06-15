from typing import Any
from llama_index.core import Document
from llama_index.core.node_parser import SentenceSplitter
import json
from modules.config import CHUNK_SIZE, CHUNK_OVERLAP

def split_json_data(profile_json:dict[str,Any]):
    
    profile_json_data = json.dumps(profile_json)
    documents = Document(text=profile_json_data)
    
    splitter = SentenceSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)
    nodes = splitter.get_nodes_from_documents(documents=documents,
                                              show_progress=True)