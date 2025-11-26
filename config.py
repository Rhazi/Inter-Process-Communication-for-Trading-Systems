from enum import Enum


#order Manager info
MANAGER_HOST = 'localhost'
MANAGER_PORT = 8000
LOG_FILE = "log_manager.log"

#Message info
MESSAGE_DELIMITER = b'*'
BYTE_LIMIT = 1024


class MessageType(Enum):
    NEWS_SENTIMENT = "NEWS_SENTIMENT"
    PRICE = "PRICE"