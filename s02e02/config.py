import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
EXCLUDED_CITIES = ["Bielsko-Biała", "Toruń", "Kraków", "Warszawa", "Olsztyn", "Bydgoszcz"]