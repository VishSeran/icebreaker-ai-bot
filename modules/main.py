from modules.models_config import init_llm_model, embedding_model
from modules.data_extraction import data_extraction
from modules.data_preprocess import (
    split_json_data,
    create_vector_database,
    verify_verctor_database,
)
from modules.query_engine import init_query_engine
from modules.logger import get_logger
import gradio as gr

logger = get_logger("main_logger")
global_query_engine = None

def process_linkedin(linkedin_url, mock_use: bool, api_key: str):
    
    global global_query_engine
    try:
        if mock_use or not api_key or not linkedin_url:
            linkedin_url = "https://www.linkedin.com/in/leonkatsnelson/"

        profile_data = data_extraction(
            linkedIn_url=linkedin_url,
            api_key=api_key if not mock_use else None,
            ismock=mock_use,
        )

        if not profile_data:
            raise ValueError("profile data are not found")

        logger.info("profile data fetched")

        llm_model = init_llm_model()

        if not llm_model:
            raise ValueError("error while creating llm model")

        logger.info("llm model created")

        embed_model = embedding_model()
        if not embed_model:
            raise ValueError("error while creating embedding model")

        logger.info("embedding model created")

        nodes = split_json_data(profile_data)

        if not nodes:
            raise ValueError("nodes are not found")

        logger.info("nodes created")

        index = create_vector_database(nodes, embed_model)

        if not index:
            raise ValueError("index is not founnd")

        logger.info("index is created")
        logger.info("index verification started")

        verify_result = verify_verctor_database(index)

        if verify_result:
            logger.info("verification sucessfull")
        else:
            logger.warning("verification failed")
        
        query_engine = init_query_engine(index,llm_model)
        
        if not query_engine:
            raise ValueError("Query engine is not found")
        
        global_query_engine = query_engine
        logger.info("query engine created")
        
        query = "Provide three interesting facts about this person\'s career"
        response = query_engine.query(query)
        return response
        
    except ValueError as e:
        logger.error(f"Value error: {e}")
        return None

    except Exception as e:
        logger.error(f"Error while fetching process: {e}")
        return None
    
def answer_user_query(user_query:str):
    
    try:

        if not user_query:
            raise ValueError("user query is empty or none")
        
        if global_query_engine is None:
            raise ValueError("System not initialized. Please load LinkedIn profile first.")
        
        answer = global_query_engine.query(user_query)
        logger.info("answer fetched sucessfull")
        return answer
    
    except ValueError as e:
        logger.error(f"Value error:{e}")
        return None
        
    except Exception as e:
        logger.error(f"Error while answering to user query: {e}")
        return None    
    
def gradio_interface():
    
    with gr.Blocks(title="LinedIn Icebraker Bot") as demo:
        
        gr.Markdown("# LinkedIn Icebreaker bot welconme")
        
        #with gr.Tab("Process LinkedIn Profile"):
            
    return demo  
        
    

if __name__ == "__main__":
    demo= gradio_interface()
    demo.launch()