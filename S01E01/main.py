from common.llm_client import LLMClient
from common.web_client import WebClient
from common.logger import setup_logger
from config import OPENAI_API_KEY, URL, USERNAME, PASSWORD
import os

# Ensure logs directory exists
os.makedirs("logs", exist_ok=True)

# Initialize logger to file and console
logger = setup_logger(logfile="logs/s01e01.log", level="DEBUG")

# Initialize clients
llm = LLMClient(api_key=OPENAI_API_KEY)
web = WebClient()

def get_question():
    logger.info("Pobieram pytanie ze strony logowania...")
    response = web.get(URL)
    import re
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
    response = web.post(URL, data=payload, headers=headers)
    html = response.text
    import re
    flag_pattern = r"\{\{FLG:([A-Z0-9_]+)\}\}"
    match = re.search(flag_pattern, html)
    if match:
        logger.success(f"Znaleziono flagę: {match.group(1)}")
        return match.group(1)
    else:
        logger.warning("Nie znaleziono flagi w odpowiedzi.")
        return None

def main():
    logger.info("Start programu S01E01")
    try:
        question = get_question()
        answer = llm.ask(question, instructions="Answer the following question briefly and precisely. Provide only the answer, without additional explanation. If asked about year, provide only a year, not the full date.")
        flag = login(answer)
    except Exception as e:
        logger.error(f"Error: {str(e)}")

if __name__ == "__main__":
    main()