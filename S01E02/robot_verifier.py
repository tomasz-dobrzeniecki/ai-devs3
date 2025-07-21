import requests
from loguru import logger
from llm_client import get_answer
from config import FETCH_URL, VERIFY_URL

session = requests.Session()

def verify_robot():
    logger.info("Fetching memory dump...")
    response = session.get(FETCH_URL)
    if response.status_code != 200:
        logger.error(f"Error while fetching the page: {response.status_code}")
        raise Exception(f"Error while fetching the page: {response.status_code}")
    memory_dump = response.text
    logger.info("Memory dump retrieved.")

    logger.info("Fetching question...")
    payload = {"text": "READY", "msgID": "0"}
    response = session.post(VERIFY_URL, json=payload)
    if response.status_code != 200:
        logger.error(f"Error while fetching the page: {response.status_code}")
        raise Exception(f"Error while fetching the page: {response.status_code}")
    data = response.json()
    logger.info("Question retrieved.")
    msg_id = str(data.get("msgID", "0"))

    while True:
        question = data.get("text")
        if not question:
            logger.error("Missing 'text' field in response")
            break
        if question == "OK":
            logger.debug("Received keep-alive OK signal.")
            continue
        if question.startswith("{{FLG:"):
            logger.success(f"Success! Found the flag: {question}")
            break
        if data.get("code") == -777:
            logger.warning("Intruder detected! Mission failed.")
            break

        logger.info(f"Answering question: {question}")
        answer = get_answer(memory_dump, question)
        payload = {"text": answer, "msgID": msg_id}
        response = session.post(VERIFY_URL, json=payload)
        response.raise_for_status()
        data = response.json()
        msg_id = str(data.get("msgID", msg_id))