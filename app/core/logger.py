import logging as std_logging


class RequestContextFilter(std_logging.Filter):
    """Filter that adds default values for request context fields when not present"""

    def filter(self, record):
        if not hasattr(record, "method"):
            record.method = "N/A"
        if not hasattr(record, "path"):
            record.path = "N/A"
        if not hasattr(record, "client"):
            record.client = "N/A"
        return True


# Create handler with the filter
handler = std_logging.StreamHandler()
handler.addFilter(RequestContextFilter())
handler.setFormatter(
    std_logging.Formatter(
        "[%(levelname)s] - %(asctime)s - %(message)s | "
        "Method = %(method)s | "
        "Path = %(path)s | "
        "Client = %(client)s | "
    )
)

# Configure root logger
std_logging.basicConfig(level=std_logging.INFO, handlers=[handler])

logger = std_logging.getLogger("egos-api")
