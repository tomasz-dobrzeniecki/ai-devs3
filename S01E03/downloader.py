import requests
from loguru import logger

def download_input_file(url: str) -> dict:
    logger.info("Downloading input data...")
    response = requests.get(url)
    response.raise_for_status()
    return response.json()
