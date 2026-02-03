import logging

logging.basicConfig(
    level=logging.INFO,
    format=(
        "[%(levelname)s] - %(asctime)s - %(message)s | "
        "Method = %(method)s | "
        "Path = %(path)s | "
        "Client = %(client)s | "
    ),
)

logger = logging.getLogger("egos-api")
