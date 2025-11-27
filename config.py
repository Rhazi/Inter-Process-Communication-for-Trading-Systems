from enum import Enum

# Server Info
SERVER_HOST = "localhost"
SERVER_PORT_GATEWAY = 8999

#order Manager info
MANAGER_HOST = 'localhost'
MANAGER_PORT = 8998
LOG_FILE = "log_manager.log"

#Message info
MESSAGE_DELIMITER = b'*'
STRING_DELIMITER = ","
BYTE_LIMIT = 1024

class MessageType(Enum):
    NEWS_SENTIMENT = "NEWS_SENTIMENT"
    PRICE = "PRICE"
    REGISTER = "REGISTER"

class ClientType(Enum):
    STRATEGY = "STRATEGY"