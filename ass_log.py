# ass_log.py
import logging

# 1. Create a dedicated, named logger for your application
logger = logging.getLogger("ghost_assistant")
logger.setLevel(logging.INFO)

# 2. Avoid duplicate logs if this file gets imported multiple times
if not logger.handlers:
    # Create a file handler to save logs to disk
    file_handler = logging.FileHandler("assistant.log")
    
    # Define a clean, professional formatting structure
    formatter = logging.Formatter(
        '%(asctime)s - [%(levelname)s] - %(filename)s:%(lineno)d - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(formatter)
    
    # Attach the handler to our custom logger
    logger.addHandler(file_handler)