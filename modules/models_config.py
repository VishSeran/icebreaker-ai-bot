from modules.config import LLM_MODEL_ID, EMBEDDING_MODEL_ID
from logging import Logger
from llama_index.llms.huggingface import HuggingFaceLLM
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

logger = Logger("logger")


def embedding_model(model_name: str = EMBEDDING_MODEL_ID):

    try:
        if not model_name:
            raise ValueError("model name is empty or none")

        embedd_model = HuggingFaceEmbedding(model_name=model_name)
        logger.info(f"embeddig model {model_name} is loaded")
        return embedd_model

    except ValueError as e:
        logger.error(f"Value error: {e}")

    except Exception as e:
        logger.error(f"Error while launching embedding model: {e}")
        print(f"Error while launching embedding model: {e}")
        return None


def init_llm_model(model_name: str = LLM_MODEL_ID):

    try:
        if not model_name:
            raise ValueError("model name is empty or none")

        model = HuggingFaceLLM(
            model_name=model_name,
            context_window=4096,
            max_new_tokens=512,
            generate_kwargs={"temperature": 0.7},
        )

        logger.info("LLM model is lanuching!!!")
        return model

    except ValueError as e:
        logger.error(f"value error: {e}")
        print(f"value error:{e}")
