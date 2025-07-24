import requests
from logger import logger
from config import DATA_URL

def fetch_data() -> str | None:
    try:
        logger.info("Starting fetching data...")
        response = requests.get(DATA_URL)
        response.raise_for_status()
        return response.text.strip()
    except requests.RequestException as e:
        logger.error(f"Error fetching data: {e}")
        return None