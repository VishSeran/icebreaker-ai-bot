from modules.models_config import init_llm_model, embedding_model
from modules.data_extraction import data_extraction
from modules.data_preprocess import split_json_data, create_vector_database, verify_verctor_database
from modules.logger import get_logger

logger = get_logger("main_logger")


def process_linkedin(linedin_url, mock_use: bool, api_key: str):

    try:
        if mock_use or not api_key or not linedin_url:
            linedin_url = "https://www.linkedin.com/in/leonkatsnelson/"

        profile_data = data_extraction(
            linkedIn_url=linedin_url,
            api_key=api_key if not mock_use else None,
            ismock=mock_use,
        )

        if not profile_data:
            raise ValueError("profile data are not found")
        
        logger.info("profile data fetched")
        
        nodes = split_json_data(profile_data)
        
        if not nodes:
            raise ValueError("nodes are not found")
        
        logger.info("nodes created")
        
        index = create_vector_database(nodes)
        
        if not index:
            raise ValueError("index are not founnd")
        
        logger.info("index are created")
        

    except ValueError as e:
        logger.error(f"Value error: {e}")
        return None

    except Exception as e:
        logger.error(f"Error while fetching process: {e}")
        return None
