from config import REPORT_URL, API_KEY
from common.data_submitter import DataSubmitter

def send_report(censored_text: str, logger) -> bool:
    payload = {
        "task": "CENZURA",
        "apikey": API_KEY,
        "answer": censored_text
    }
    try:
        submitter = DataSubmitter()
        response = submitter.submit_json(REPORT_URL, payload)
        data = response.json()
        logger.info(f"API response: {data}")
        return data.get("message", "").startswith("{{FLG:")
    except Exception as e:
        logger.error(f"Error sending report: {e}")
        return False