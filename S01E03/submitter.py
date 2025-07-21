import requests
from config import API_KEY, SUBMIT_URL
from loguru import logger

def submit_payload(original_data: dict, corrected_data: list[dict]):
    payload = {
        "task": "JSON",
        "apikey": API_KEY,
        "answer": {
            "apikey": API_KEY,
            "description": original_data.get("description"),
            "copyright": original_data.get("copyright"),
            "test-data": corrected_data
        }
    }

    logger.info("Submitting corrected data...")
    response = requests.post(SUBMIT_URL, json=payload)
    logger.success(f"Status code: {response.status_code}")
    logger.debug(f"Response: {response.text}")
