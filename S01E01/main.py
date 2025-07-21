from web_client import get_question, login
from llm_client import get_answer
from loguru import logger

def main():
    logger.info("Start programu S01E01")
    try:
        question = get_question()
        answer = get_answer(question)
        flag = login(answer)
    except Exception as e:
        logger.error(f"Error: {str(e)}")

if __name__ == "__main__":
    main()