import os
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
FETCH_URL = "https://xyz.ag3nts.org/files/0_13_4b.txt"
VERIFY_URL = "https://xyz.ag3nts.org/verify"