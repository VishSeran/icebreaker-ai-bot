from modules.models_config import init_llm_model, embedding_model
from modules.data_extraction import data_extraction
from modules.data_preprocess import (
    split_json_data,
    create_vector_database,
    verify_verctor_database,
)
from modules.query_engine import init_query_engine, answer_user_query
from modules.logger import get_logger

logger = get_logger("main_logger")


def process_linkedin(linkedin_url, mock_use: bool, api_key: str):

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
        
        logger.info("query engine created")
        
         
            

    except ValueError as e:
        logger.error(f"Value error: {e}")
        return None

    except Exception as e:
        logger.error(f"Error while fetching process: {e}")
        return None
