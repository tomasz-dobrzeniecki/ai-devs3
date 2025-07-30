import requests
from loguru import logger

class WebClient:
    def __init__(self):
        self.session = requests.Session()

    def get(self, url, **kwargs):
        logger.info(f"GET {url}")
        response = self.session.get(url, **kwargs)
        logger.debug(f"Status code: {response.status_code}")
        response.raise_for_status()
        return response

    def post(self, url, data=None, json=None, headers=None, **kwargs):
        logger.info(f"POST {url}")
        response = self.session.post(url, data=data, json=json, headers=headers, **kwargs)
        logger.debug(f"Status code: {response.status_code}")
        response.raise_for_status()
        return response 