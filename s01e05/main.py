from config import POLL_INTERVAL, OPENAI_API_KEY
from fetcher import fetch_data
from censor_prompt import build_prompt
from reporter import send_report
from common.llm_client import LLMClient
from common.logger import setup_logger
import os
import time
import sys

# Ensure logs directory exists
os.makedirs("logs", exist_ok=True)

# Initialize logger
logger = setup_logger(logfile="logs/s01e05.log", level="DEBUG")

llm = LLMClient(api_key=OPENAI_API_KEY)

def main():
    while True:
        try:
            raw = fetch_data(logger)
            if raw:
                logger.debug("Data fetched successfully.")
                prompt = build_prompt(raw)
                logger.debug(f"Prompt built.")

                logger.info("Sending request to OpenAI API...")
                response = llm.ask(prompt, temperature=0)
                censored = response
                logger.debug(f"Received response.")

                logger.info("Sending report to server...")
                if send_report(censored, logger):
                    logger.success("Flag found and reported!")
                    sys.exit(0)
                else:
                    logger.warning("Report was not accepted by the server.")
            else:
                logger.info("No new data fetched.")
            logger.info(f"Sleeping for {POLL_INTERVAL} seconds.")
            time.sleep(POLL_INTERVAL)
        except Exception as e:
            logger.exception(f"Unexpected error: {e}")
            logger.info(f"Sleeping for {POLL_INTERVAL} seconds after error.")
            time.sleep(POLL_INTERVAL)

if __name__ == "__main__":
    main()