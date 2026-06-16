from llama_index.core import VectorStoreIndex
from logging import Logger
from modules.config import SIMILARITY_TOP_K, USER_QUESTION_TEMPLATE
from llama_index.core.prompts import PromptTemplate

logger = Logger("logger")

def init_query_engine(index:VectorStoreIndex, llm_model):
    
    try:
        if not USER_QUESTION_TEMPLATE:
            raise ValueError ("User query prompt template is empty or none")
        
        prompt_template = PromptTemplate(template=USER_QUESTION_TEMPLATE)
        
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

  
def answer_user_query(user_query:str, query_engine):
    
    try:
        if not user_query:
            raise ValueError("user query is empty or none")
        
        answer = query_engine.query(user_query)
        logger.info("answer fetched sucessfull")
        return answer
    
    except ValueError as e:
        logger.error(f"Value error:{e}")
        return None
        
    except Exception as e:
        logger.error(f"Error while answering to user query: {e}")
        return None