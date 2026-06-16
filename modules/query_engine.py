from typing import Optional
from llama_index.core import VectorStoreIndex
from logging import Logger
from modules.data_preprocess import create_vector_database
from modules.models_config import llm_model

logger = Logger("logger")



def query_engine(index:VectorStoreIndex):
    
    try:
        query_engine = index.as_query_engine(
            
        )
        
    except Exception as e:
        logger.error(f"Error while launching query engine: {e}")        
        return None