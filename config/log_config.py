# config/log_config.py
import logging


def setup_logging():
    logging.basicConfig(
        filename='app.log',
        level=logging.DEBUG,
        format='{"time": "%(asctime)s", "level": "%(levelname)s", "message": "%(message)s"}',
        datefmt="%Y-%m-%dT%H:%M:%S%z"
    )