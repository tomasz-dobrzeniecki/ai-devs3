import requests
import json
from loguru import logger

def submit_answer(answer: str, apikey: str):
    url = "https://c3ntrala.ag3nts.org/report"
    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "Accept": "application/json"
    }
    payload = {
        "task": "mp3",
        "apikey": apikey,
        "answer": answer
    }

    try:
        logger.info(f"Sending response...")
        payload_bytes = json.dumps(payload, ensure_ascii=False).encode('utf-8')
        response = requests.post(
            url, 
            data=payload_bytes,  # Send as bytes instead of json parameter
            headers=headers,
            verify=True
        )
        response.raise_for_status()
        data = response.json()
        
        logger.info(f"API response: {data}")
        return data.get("message", "").startswith("{{FLG:")
    except requests.RequestException as e:
        
        logger.error(f"Error sending report: {e}")
        return False