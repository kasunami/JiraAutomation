import json
import logging
import log_config

# Configure Logging
log_config.setup_logging()  # Call to set up default logging configuration.
logger = logging.getLogger(__name__)


def validate_config(config_file):
    """Validates the structure of the config.json file."""
    logger.debug(f"Starting config validation for {config_file}")
    try:
        with open(config_file, 'r') as f:
            config = json.load(f)
            logger.debug("Config file loaded successfully")

        if "statuses" not in config or len(config["statuses"]) < 2:
            logger.error("Config file must contain a 'statuses' list with at least two entries.")
            return False

        for status in config["statuses"]:
            if "name" not in status or "id" not in status:
                logger.error("Each item in 'statuses' must have a 'name' and 'id' field.")
                return False

        logger.info("Config file validated successfully.")
        return True

    except (FileNotFoundError, json.JSONDecodeError) as e:
        logger.exception(f"Error loading or parsing the config file: {e}")  # Logs exception details
        return False