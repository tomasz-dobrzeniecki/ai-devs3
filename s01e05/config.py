import os
from dotenv import load_dotenv

load_dotenv()

DATA_URL = "https://c3ntrala.ag3nts.org/data/7f6ff94a-ced2-46e2-8c90-aa4fdec3b948/cenzura.txt"
REPORT_URL = "https://c3ntrala.ag3nts.org/report"
API_KEY = "7f6ff94a-ced2-46e2-8c90-aa4fdec3b948"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
POLL_INTERVAL = 60