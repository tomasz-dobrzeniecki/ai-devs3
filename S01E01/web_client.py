import requests
import re
from config import URL, USERNAME, PASSWORD
from loguru import logger

session = requests.Session()

def get_question():
    
    logger.info("Pobieram pytanie ze strony logowania...")
    response = session.get(URL)
    
    logger.debug(f"Status odpowiedzi GET: {response.status_code}")
    if response.status_code != 200:
        logger.error(f"Error while fetching the page: {response.status_code}")
        raise Exception(f"Error while fetching the page: {response.status_code}")
    
    html = response.text
    pattern = r'<p[^>]*id="human-question"[^>]*>(.*?)</p>'
    match = re.search(pattern, html, re.DOTALL)
    if not match:
        logger.error("Nie znaleziono pytania w HTML!")
        raise Exception("Nie znaleziono pytania w HTML!")
    question = match.group(1).strip()
    question = re.sub(r'<[^>]+>', '', question)
    logger.debug(f"Treść pytania: {question}")
    return question

def login(answer):
    logger.info("Próbuję zalogować się do systemu...")
    payload = {
        "username": USERNAME,
        "password": PASSWORD,
        "answer": answer
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    response = session.post(URL, data=payload, headers=headers)
    logger.debug(f"Status odpowiedzi POST: {response.status_code}")
    if response.status_code != 200:
        logger.error(f"Login failed with status code: {response.status_code}")
        raise Exception(f"Login failed with status code: {response.status_code}")
    
    html = response.text
    flag_pattern = r"\{\{FLG:([A-Z0-9_]+)\}\}"
    match = re.search(flag_pattern, html)
    if match:
        logger.success(f"Znaleziono flagę: {match.group(1)}")
        return match.group(1)
    else:
        logger.warning("Nie znaleziono flagi w odpowiedzi.")
        return None