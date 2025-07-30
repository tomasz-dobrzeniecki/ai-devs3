from config import DATA_URL
from common.data_fetcher import DataFetcher

def fetch_data(logger) -> str | None:
    try:
        logger.info("Starting fetching data...")
        fetcher = DataFetcher()
        response = fetcher.fetch_text(DATA_URL)
        return response.strip()
    except Exception as e:
        logger.error(f"Error fetching data: {e}")
        return None