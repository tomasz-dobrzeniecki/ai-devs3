from .web_client import WebClient
from loguru import logger

class DataFetcher:
    def __init__(self):
        self.client = WebClient()

    def fetch_json(self, url):
        logger.info(f"Fetching JSON from {url}")
        response = self.client.get(url)
        return response.json()

    def fetch_text(self, url):
        logger.info(f"Fetching text from {url}")
        response = self.client.get(url)
        return response.text 