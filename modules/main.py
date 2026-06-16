from modules.models_config import init_llm_model, embedding_model
from modules.data_extraction import data_extraction
from modules.data_preprocess import (
    split_json_data,
    create_vector_database,
    verify_verctor_database,
)
from modules.query_engine import init_query_engine
from modules.logger import get_logger
from llama_index.core.prompts import PromptTemplate
from modules.config import USER_QUESTION_TEMPLATE,SIMILARITY_TOP_K
import gradio as gr

logger = get_logger("main_logger")

global_query_engine = None
global_llm_model = None
global_index = None

def process_linkedin(linkedin_url, api_key: str, mock_use: bool):
    
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
        
        global_llm_model = llm_model

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
        
        global_index = index

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
        logger.info(f"Response: {response}")
        return response
        
    except ValueError as e:
        logger.error(f"Value error: {e}")
        return f"ERROR: {str(e)}"

    except Exception as e:
        logger.error(f"Error while fetching process: {e}")
        return f"ERROR: {str(e)}"
    
def answer_user_query(user_query:str):
    
    try:

        if not user_query:
            raise ValueError("user query is empty or none")
        
        
        
        if not USER_QUESTION_TEMPLATE:
            raise ValueError ("User query prompt template is empty or none")
        
        prompt_template = PromptTemplate(template=USER_QUESTION_TEMPLATE)
        
        query_engine = global_index.as_query_engine(
            llm=global_llm_model,
            streaming=False,
            similarity_top_k=SIMILARITY_TOP_K,
            text_qa_template=prompt_template
        )
        
        answer = query_engine.query(user_query)
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
        
        gr.Markdown("# LinedIn Icebraker Bot")
        
        with gr.Tab("Process LinkedIn Profile"):
            with gr.Row():
                with gr.Column():
                    linkedin_url = gr.Textbox(
                        label="LinedIn Profile URL",
                        placeholder="https://www.linkedin.com/in/username/"
                    )
                    
                    api_key = gr.Textbox(
                        label="enter your api key (leave empty for mock test)",
                        placeholder="Your ProxyCurl API Key",
                        type="password",
                        
                    )
                    
                    mock_use = gr.Checkbox(label="Use mock data",
                                           value=True)
                    
                    process_btn = gr.Button("Process Profile")
                
                with gr.Column():
                    result_txt = gr.Textbox(label="Initial Facts", lines=10)
                
                process_btn.click(
                    fn=process_linkedin,
                    inputs=[linkedin_url, api_key, mock_use],
                    outputs=[result_txt]
                )
        
        with gr.Tab(label="Chat with Bot"):
            gr.Markdown("# Chat with the processed LinkedIn profile")
            
            chatbot = gr.Chatbot(height=600)
            chat_input = gr.Textbox(
                label="Ask question about the profile",
                placeholder="What is this person's current job title?"
            )
            
            chat_btn = gr.Button("Send")
            
            chat_btn.click(
                fn= answer_user_query,
                inputs=[chat_input,chatbot],
                outputs=[chatbot]
            )
            
            chat_input.submit(
                fn=answer_user_query,
                inputs=[chat_input,chatbot],
                outputs=[chatbot]
            )
                
    return demo  
        
    

if __name__ == "__main__":
    demo= gradio_interface()
    demo.launch()