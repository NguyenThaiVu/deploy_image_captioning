import os 
import logging


def create_logger():

    log_dir = 'logs'
    os.makedirs(log_dir, exist_ok=True)


    # Create a logger
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)  # Set the overall logger level

    # Create an INFO file handler
    info_handler = logging.FileHandler(os.path.join(log_dir, 'server_info.log'))
    info_handler.setLevel(logging.INFO)  # Log only INFO and above
    info_formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
    info_handler.setFormatter(info_formatter)

    # Create an ERROR file handler
    error_handler = logging.FileHandler(os.path.join(log_dir, 'server_error.log'))
    error_handler.setLevel(logging.ERROR)  # Log only ERROR and above
    error_formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
    error_handler.setFormatter(error_formatter)

    # Add handlers to the logger
    logger.addHandler(info_handler)
    logger.addHandler(error_handler)

    # Example usage
    # logger.info("This is an info log.")
    # logger.error("This is an error log.")
    
    return logger