import logging

from edge_traffic.config import get_settings
from edge_traffic.logging import setup_logging


def main() -> None:
    settings = get_settings()
    setup_logging(settings)

    logger = logging.getLogger(__name__)
    logger.info(
        "worker started app_name=%s env=%s",
        settings.app_name,
        settings.environment,
    )


if __name__ == "__main__":
    main()
