import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
API_KEY = os.getenv("API_KEY")
BASE_URL = os.getenv("BASE_URL")
DOWNLOAD_URL = f"{BASE_URL}/data/{API_KEY}/json.txt"
SUBMIT_URL = f"{BASE_URL}/report"