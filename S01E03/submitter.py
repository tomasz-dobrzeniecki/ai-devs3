from config import API_KEY, SUBMIT_URL
from common.data_submitter import DataSubmitter

def submit_payload(original_data: dict, corrected_data: list[dict], logger):
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
    submitter = DataSubmitter()
    response = submitter.submit_json(SUBMIT_URL, payload)
    logger.success(f"Status code: {response.status_code}")
    logger.debug(f"Response: {response.text}")