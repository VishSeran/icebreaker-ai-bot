from modules.config import LLM_MODEL_ID
from logging import Logger
from llama_index.llms.huggingface import HuggingFaceLLM

logger = Logger("logger")

def llm_model(model_name:str=LLM_MODEL_ID):
    
    try:
        if not model_name:
            raise ValueError ("model name is empty or none")
        
        model = HuggingFaceLLM(
            model_name=model_name,
            context_window=4096,
            max_new_tokens=512,
            generate_kwargs={
                "temperature": 0.7
            }
        )
        
    
    except ValueError as e:
        logger.error(f"value error: {e}")
        print(f"value error:{e}")