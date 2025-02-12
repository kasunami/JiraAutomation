# jira_api.py
import os
import requests
from dotenv import load_dotenv
import base64
import logging

from config import log_config

dotenv_path = os.path.join(os.path.dirname(__file__), 'config/.env')
load_dotenv(dotenv_path=dotenv_path)

# Configure Logging
log_config.setup_logging()  # Call to set up default logging configuration.
logger = logging.getLogger(__name__)

# Environment variables: JIRA credentials
JIRA_TOKEN = os.getenv("JIRA_TOKEN")
JIRA_USERNAME = os.getenv("JIRA_USERNAME")
JIRA_SITE_URL = os.getenv("JIRA_SITE_URL")

if not JIRA_TOKEN or not JIRA_USERNAME or not JIRA_SITE_URL:
    logger.error("Missing required environment variables")
    raise RuntimeError("Missing required environment variables: JIRA_TOKEN, JIRA_USERNAME, JIRA_SITE_URL.")

# Jira REST API endpoints
JIRA_SEARCH_ENDPOINT = f"{JIRA_SITE_URL.rstrip('/')}/rest/api/2/search"
JIRA_TRANSITIONS_ENDPOINT = f"{JIRA_SITE_URL.rstrip('/')}/rest/api/2/issue/{{issueIdOrKey}}/transitions"

# Basic Header Authorization
auth = base64.b64encode(f"{JIRA_USERNAME}:{JIRA_TOKEN}".encode()).decode()
HEADERS = {
    "Authorization": f"Basic {auth}",
    "Content-Type": "application/json",
    "Accept": "application/json"
}


def get_tickets():
    """Retrieve all tickets assigned to the current user."""
    try:
        logger.info("Fetching tickets assigned to the current user")
        response = requests.get(JIRA_SEARCH_ENDPOINT, headers=HEADERS, params={"jql": "assignee = currentUser()"})
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        tickets = response.json().get("issues", [])
        logger.debug(f"Tickets fetched successfully: {len(tickets)} tickets")
        return tickets

    except requests.RequestException as e:
        logger.exception("Error retrieving tickets", exc_info=True)
        raise


def get_ticket_transitions(ticket_key):
    """Retrieve available transitions for the given ticket."""
    try:
        logger.info(f"Fetching transitions for ticket {ticket_key}")
        url = JIRA_TRANSITIONS_ENDPOINT.format(issueIdOrKey=ticket_key)
        response = requests.get(url, headers=HEADERS, params={"sortByOpsBarAndStatus": "true"})
        response.raise_for_status()
        transitions = response.json().get("transitions", [])
        logger.debug(f"Transitions fetched for ticket {ticket_key}: {transitions}")
        return transitions
    except requests.RequestException as e:
        logger.exception(f"Error retrieving transitions for ticket {ticket_key}", exc_info=True)
        raise


def move_ticket_to_status(ticket_key, transition_id):
    """Move a ticket to the specified status."""
    try:
        logger.info(f"Transitioning ticket {ticket_key} using transition ID {transition_id}")
        url = JIRA_TRANSITIONS_ENDPOINT.format(issueIdOrKey=ticket_key)
        payload = {"transition": {"id": transition_id}}
        response = requests.post(url, headers=HEADERS, json=payload)
        response.raise_for_status()
        logger.info(
            f"Successfully transitioned ticket {ticket_key} to transition ID {transition_id}")  # Include transition ID
    except requests.RequestException as e:
        logger.exception(f"Failed to transition ticket {ticket_key} to transition ID {transition_id}", exc_info=True)
        raise
