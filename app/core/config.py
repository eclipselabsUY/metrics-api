from dotenv import load_dotenv
import os

# ENV VAR

load_dotenv(dotenv_path=os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env"))

# Services

SERVICES = [
    {"name": "www.ego-services.com", "type": "http", "url": "https://www.ego-services.com"},
    {"name": "backdoor.ego-services.com", "type": "http", "url": "https://backdoor.ego-services.com/health"},
    {"name": "fingcraft.ego-services.com", "type": "tcp", "host": "fingcraft.ego-services.com", "port": 25565},
    {"name": "ssh.ego-services.com", "type": "tcp", "host": "ssh.ego-services.com", "port": 22},
]

API_KEY = os.getenv("API_KEY")

RCON_PASSWORD = os.getenv("RCON_PASSWORD")