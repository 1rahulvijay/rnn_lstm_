import logging
import os
from logging.handlers import TimedRotatingFileHandler

def app_logger(name: str) -> logging.Logger:
    try:
        path = os.path.dirname(os.path.realpath(__file__))
        log_dir = os.path.join(path, "logs")
        log_file = os.path.join(log_dir, f"{name}.log")
        if not os.path.exists(log_dir):
            os.mkdir(log_dir)

        file_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        console_formatter = logging.Formatter("%(levelname)s -- %(message)s")

        # TimedRotatingFileHandler to rotate logs daily and keep only the last 10 days
        file_handler = TimedRotatingFileHandler(log_file, when='midnight', interval=1, backupCount=10)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(file_formatter)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)  # Adjust the level to your preference
        console_handler.setFormatter(console_formatter)

        logger = logging.getLogger(name)
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        logger.setLevel(logging.DEBUG)
        
        return logger
    except OSError:
        raise RuntimeError("Unable to Load App Logger")

# Example usage
if __name__ == "__main__":
    logger = app_logger("example_app")
    logger.info("This is an info message")
    logger.debug("This is a debug message")
    logger.error("This is an error message")
