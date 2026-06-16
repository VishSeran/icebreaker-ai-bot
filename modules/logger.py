import logging

def get_logger(name:str):
    
    try:
        if not name:
            raise ValueError("name is empty or none")
        
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        
        logger = logging.getLogger(name)
        return logger
    
    except ValueError as e:
        print(f"Value error: {e}")
        return None

    except Exception as e:
        print(f"Unknown error: {e}")
        return None