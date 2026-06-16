from llama_index.core import VectorStoreIndex
from modules.logger import get_logger
from modules.config import SIMILARITY_TOP_K, USER_QUESTION_TEMPLATE,INITIAL_FACTS_TEMPLATE
from llama_index.core.prompts import PromptTemplate

logger = get_logger("query_engine_logger")

def init_query_engine(index:VectorStoreIndex, llm_model):
    
    try:
        if not USER_QUESTION_TEMPLATE:
            raise ValueError ("User query prompt template is empty or none")
        
        prompt_template = PromptTemplate(template=INITIAL_FACTS_TEMPLATE)
        
        query_engine = index.as_query_engine(
            llm=llm_model,
            streaming=False,
            similarity_top_k=SIMILARITY_TOP_K,
            text_qa_template=prompt_template
        )
        logger.info("Launch the query engine")
        return query_engine
    
    except ValueError as e:
        logger.error(f"Value error: {e}")
        return None
    
    except Exception as e:
        logger.error(f"Error while launching query engine: {e}")        
        return None

  
