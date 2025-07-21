import os
import requests
from dotenv import load_dotenv
from loguru import logger

# Load API key
load_dotenv()
DEVS_API_KEY = os.getenv("DEVS_API_KEY")
if not DEVS_API_KEY:
    logger.error("Missing DEVS_API_KEY in .env file")
    raise ValueError("Missing DEVS_API_KEY in .env file")

# URLs
BASE_URL = "https://c3ntrala.ag3nts.org"
ARTICLE_URL = f"{BASE_URL}/dane/arxiv-draft.html"
QUESTIONS_URL = f"{BASE_URL}/data/{DEVS_API_KEY}/arxiv.txt"

def fetch_article():
    """Download the article from the given URL."""
    try:
        logger.info("Downloading article from {}", ARTICLE_URL)
        response = requests.get(ARTICLE_URL)
        response.raise_for_status()
        
        # Basic validation
        content = response.text
        if not content:
            logger.error("Downloaded article is empty")
            raise ValueError("Downloaded article is empty")
            
        logger.success("Successfully downloaded article ({} characters)", len(content))
        return content
        
    except requests.RequestException as e:
        logger.exception("Failed to download article")
        raise

def fetch_questions():
    """Download questions from the given URL."""
    try:
        logger.info("Downloading questions from {}", QUESTIONS_URL)
        response = requests.get(QUESTIONS_URL)
        response.raise_for_status()
        
        # Get and validate questions
        content = response.text.strip()
        if not content:
            logger.error("Downloaded questions are empty")
            raise ValueError("Downloaded questions are empty")
            
        questions = [q.strip() for q in content.splitlines() if q.strip()]
        if not questions:
            logger.error("No questions found in the response")
            raise ValueError("No questions found in the response")
            
        logger.success("Successfully downloaded {} questions", len(questions))
        return questions
        
    except requests.RequestException as e:
        logger.exception("Failed to download questions")
        raise 