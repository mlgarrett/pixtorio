import logging
import socket
from datetime import datetime

class PixtorioLogger:
    def __init__(self, log_file_path='pixtorio.log'):
        self.log_file_path = log_file_path
        self.logger = logging.getLogger('custom_logger')
        self.logger.setLevel(logging.DEBUG)
        self.setup_logger()

    def setup_logger(self):
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler = logging.FileHandler(self.log_file_path)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

    def log_message(self, ip_address, log_level=logging.INFO):
        log_entry = f"{ip_address}"
        if log_level == logging.INFO:
            self.logger.info(log_entry)
        elif log_level == logging.ERROR:
            self.logger.error(log_entry)
        else:
            raise ValueError("Invalid log level. Use logging.INFO or logging.ERROR.")

if __name__ == "__main__":
    # Example usage:
    logger = PixtorioLogger()

    logger.log_message("127.0.0.1", log_level=logging.INFO)
    logger.log_message("127.0.0.1", log_level=logging.ERROR)

    # After running the script, check the contents of 'pixtorio.log'
