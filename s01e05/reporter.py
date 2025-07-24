import requests
from logger import logger
from config import REPORT_URL, API_KEY

def send_report(censored_text: str) -> bool:
    payload = {
        "task": "CENZURA",
        "apikey": API_KEY,
        "answer": censored_text
    }

    try:
        response = requests.post(REPORT_URL, json=payload)
        response.raise_for_status()
        data = response.json()
        logger.info(f"API response: {data}")
        return data.get("message", "").startswith("{{FLG:")
    except requests.RequestException as e:
        logger.error(f"Error sending report: {e}")
        return False