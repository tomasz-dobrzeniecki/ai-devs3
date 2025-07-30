from config import CENTRALA_KEY, OPENAI_API_KEY
from transcription import get_all_transcriptions
from prompt_builder import create_prompt
from extract import extract_street_name
from common.llm_client import LLMClient
from common.logger import setup_logger
from common.data_submitter import DataSubmitter
import os

# Ensure logs directory exists
os.makedirs("logs", exist_ok=True)

# Initialize logger
logger = setup_logger(logfile="logs/s02e01.log", level="DEBUG")

# Initialize shared clients
llm = LLMClient(api_key=OPENAI_API_KEY)
submitter = DataSubmitter()

def main():
    transcriptions = get_all_transcriptions("audio", logger)
    prompt = create_prompt(transcriptions)
    
    logger.info("Sending prompt to LLM...")
    response = llm.ask(prompt, temperature=0.7)
    logger.debug(f"LLM response: {response}")
    print(response)

    street = extract_street_name(response)
    if street:
        logger.info(f"Extracted street: {street}")
        url = "https://c3ntrala.ag3nts.org/report"
        payload = {
            "task": "mp3",
            "apikey": CENTRALA_KEY,
            "answer": street
        }
        headers = {
            "Content-Type": "application/json; charset=utf-8",
            "Accept": "application/json"
        }
        
        try:
            response = submitter.submit_json(url, payload, headers)
            data = response.json()
            logger.info(f"API response: {data}")
            if data.get("message", "").startswith("{{FLG:"):
                logger.success("Flag found!")
            else:
                logger.warning("No flag in response")
        except Exception as e:
            logger.error(f"Error sending report: {e}")
    else:
        logger.warning("No street name extracted from response")

if __name__ == "__main__":
    main()