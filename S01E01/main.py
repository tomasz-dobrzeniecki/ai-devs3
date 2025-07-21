from web_client import get_question, login
from llm_client import get_answer
from loguru import logger

def main():
    logger.info("Start programu S01E01")
    try:
        question = get_question()
        logger.debug(f"Pobrano pytanie: {question}")
        answer = get_answer(question)
        logger.debug(f"Odpowiedź z LLM: {answer}")
        flag = login(answer)
        if flag:
            logger.success(f"Znaleziono flagę: {flag}")
        else:
            logger.warning("Nie znaleziono flagi w odpowiedzi.")
    except Exception as e:
        logger.error(f"Error: {str(e)}")

if __name__ == "__main__":
    main()