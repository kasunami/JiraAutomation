# main.py
import sys
import json
import logging

import requests

from api import jira_api
from config import config_validator, log_config

# Configure Logging
log_config.setup_logging()
logger = logging.getLogger(__name__)


def filter_tickets(tickets, criteria, include=True):
    """Filters tickets based on include/exclude criteria.  Logs the criteria used."""
    logger.debug(f"Filtering tickets with criteria: {criteria}, include={include}")  # Log the criteria
    filtered_tickets = []
    for ticket in tickets:
        matches = all(ticket.get(key) == value for key, value in criteria.items())
        if (include and matches) or (not include and not matches):
            filtered_tickets.append(ticket)
    return filtered_tickets


def main(config_file="config/config.json"):
    """Main execution process."""
    logger.info("Application started")
    try:
        if not config_validator.validate_config(config_file):
            return  # Exit if config is invalid

        try:
            with open(config_file, 'r') as f:
                config = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            logger.exception(f"Error loading config file: {e}")
            return  # Let the user know if their config.json could not be loaded

        # Check for completely empty or invalid config structure
        if not config or not isinstance(config.get("include"), dict) or not isinstance(config.get("exclude"), dict):
            logger.error("Invalid config file structure. 'include' and 'exclude' must be dictionaries (even if empty).")
            return

        try:
            all_tickets = jira_api.get_tickets()
            logger.debug(f"Retrieved {len(all_tickets)} tickets from Jira.")

            included_tickets = filter_tickets(all_tickets, config.get("include", {}), include=True)
            excluded_tickets = filter_tickets(included_tickets, config.get("exclude", {}), include=False)

            logger.info(f"Included tickets: {included_tickets}")
            logger.info(f"Excluded tickets after filtering: {excluded_tickets}")


        except requests.exceptions.RequestException as e:  # Handle Jira API errors
            logger.exception(f"A Jira API error occurred: {e}")
            return

        logger.info("Application finished successfully")


    except Exception as e:  # Catches any other unexpected errors.
        logger.exception(f"An unexpected error occurred: {e}", exc_info=True)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        config_file_path = sys.argv[1]
        main(config_file_path)
    else:
        main()