from .web_client import WebClient
from loguru import logger

class DataSubmitter:
    def __init__(self):
        self.client = WebClient()

    def submit_json(self, url, payload, headers=None):
        logger.info(f"Submitting JSON to {url}")
        response = self.client.post(url, json=payload, headers=headers)
        logger.debug(f"Response: {response.text}")
        return response

    def submit_form(self, url, data, headers=None):
        logger.info(f"Submitting form to {url}")
        response = self.client.post(url, data=data, headers=headers)
        logger.debug(f"Response: {response.text}")
        return response 