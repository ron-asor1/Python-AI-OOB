# src/utils/logger_setup.py
import logging
import os
from datetime import datetime

def setup_logging():
    """
    Configures the logging for the application, outputting to console and a file.
    """
    log_dir = "data/logs"
    os.makedirs(log_dir, exist_ok=True)
    log_filename = datetime.now().strftime("app_%Y-%m-%d_%H-%M-%S.log")
    log_filepath = os.path.join(log_dir, log_filename)

    # Base logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO) # Set the base logging level

    # Remove existing handlers to prevent duplicate logs on successive calls
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    # Console Handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter('%(levelname)s [%(name)s] %(message)s')
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    # File Handler
    file_handler = logging.FileHandler(log_filepath)
    file_handler.setLevel(logging.INFO)
    file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - [%(name)s] - %(message)s')
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

    # Set specific log levels for chatty libraries if needed
    logging.getLogger('browser_use').setLevel(logging.INFO)
    logging.getLogger('httpx').setLevel(logging.WARNING) # Often chatty with requests
    logging.getLogger('httpcore').setLevel(logging.WARNING) # Often chatty with requests

    logging.info(f"Logging configured. Logs will be saved to: {log_filepath}")