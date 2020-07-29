
from enum import Enum

class MessageType(Enum):
    NEW_BUFFER = 1
    EXTEND_BUFFER = 2
    DELETE_BUFFER = 3
    REQUEST_REPONSES = 4
