import logging
import os
logger = logging.getLogger(__name__)
LOG_DIR  = os.path.join(os.getcwd(), "logs")

def setup_logger():
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)
    log_file_path = os.path.join(LOG_DIR, "logfile.log")
    logging.basicConfig(level=logging.DEBUG, 
                        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                        datefmt="%Y-%m-%d %H:%M:%S",
                        handlers=[
                            logging.FileHandler(log_file_path),
                            logging.StreamHandler()
                        ])

    logger.info("Logger has been set up.")
