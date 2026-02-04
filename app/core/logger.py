import logging as std_logging

std_logging.basicConfig(
    level=std_logging.INFO,
    format=(
        "[%(levelname)s] - %(asctime)s - %(message)s | "
        "Method = %(method)s | "
        "Path = %(path)s | "
        "Client = %(client)s | "
    ),
)

logger = std_logging.getLogger("egos-api")
