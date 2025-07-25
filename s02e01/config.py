import os
from dotenv import load_dotenv
from openai import OpenAI
from loguru import logger

load_dotenv()

logger.add("logs/app.log", rotation="1 MB")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
CENTRALA_KEY = os.getenv("CENTRALA_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)