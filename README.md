# Project README

## Overview

This project automates the process of filtering and managing Jira tickets based on criteria specified in a configuration file (`config.json`). It uses the Jira API to interact with Jira and the standard Python `logging` module to track progress and errors.

## Setup

1.  **Clone the repository:**

    ```bash
    git clone <repository_url>
    ```
2.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```
3.  **Create .env file:**

    Create a `.env` file in the *config* directory of the project. This file should contain your Jira API credentials and other sensitive information. A `.gitignore` file is already included, ensuring this file will not be committed to the repository.

    Use the `sample.env` file as a template, replacing the placeholder values with your actual credentials.
4.  **Environment Variables:**

    The following environment variables are required in the `.env` file:

    ```
    JIRA_SITE_URL="your_jira_site_url"
    JIRA_USERNAME="your_jira_username"
    JIRA_TOKEN="your_jira_api_token"
    ```

## Usage

Run the main script:

```bash
python main.py  # Uses config/config.json by default.
```

You can optionally specify a different config file:

```bash
python main.py <path_to_config_file> 
```

The script will fetch all tickets assigned to the user specified in the `.env` file, filter them according to `config.json` and log its actions.  The progress and any errors will be logged to `app.log`.