import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
CENTRALA_KEY = os.getenv("CENTRALA_API_KEY")