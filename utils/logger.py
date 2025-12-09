import logging
import os
import sys
from datetime import datetime

LOGS_DIR = "logs"
os.makedirs(LOGS_DIR, exist_ok=True)

LOG_FILE = os.path.join(LOGS_DIR, f"log_{datetime.now().strftime('%Y-%m-%d')}.log")
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

class LogColors:
    RESET = '\033[0m'
    BLUE = '\033[94m'      # INFO
    GREEN = '\033[92m'     # DEBUG
    YELLOW = '\033[93m'    # WARNING
    RED = '\033[91m'       # ERROR
    MAGENTA = '\033[95m'   # CRITICAL
    BOLD = '\033[1m'
class ColoredFormatter(logging.Formatter):
   
    COLORS = {
        'DEBUG': LogColors.GREEN,
        'INFO': LogColors.BLUE,
        'WARNING': LogColors.YELLOW,
        'ERROR': LogColors.RED,
        'CRITICAL': LogColors.MAGENTA + LogColors.BOLD,
    }
    
    def format(self, record):
        levelname_original = record.levelname
        
        if record.levelname in self.COLORS:
            record.levelname = f"{self.COLORS[record.levelname]}{record.levelname}{LogColors.RESET}"
        
        formatted = super().format(record)
        record.levelname = levelname_original
        
        return formatted

def get_logger(name):

    logger = logging.getLogger(name)
    if logger.handlers:
        return logger
    
    logger.setLevel(logging.INFO)
    
    file_handler = logging.FileHandler(LOG_FILE)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter(LOG_FORMAT))
    
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(ColoredFormatter(LOG_FORMAT))
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger