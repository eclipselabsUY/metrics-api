from enum import Enum

class ServiceKind(str, Enum):
    FRONTEND = "frontend"
    BACKEND = "backend"
