import logging
import os
from datetime import datetime

# Creates logs directory
os.makedirs("logs", exist_ok=True)

def setup_logger(name: str):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    # Check if handlers already exist to avoid duplicates
    if not logger.handlers:
        # File Handler
        timestamp = datetime.now().strftime("%Y-%m-%d")
        file_handler = logging.FileHandler(f"logs/app_{timestamp}.log")
        file_handler.setLevel(logging.INFO)
        
        # Console Handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # Formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        
    return logger
