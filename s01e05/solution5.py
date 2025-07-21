import requests
import json
import time
import logging
from openai import OpenAI
from dotenv import load_dotenv
import os
import sys

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuration
DATA_URL = "https://c3ntrala.ag3nts.org/data/7f6ff94a-ced2-46e2-8c90-aa4fdec3b948/cenzura.txt"
REPORT_URL = "https://c3ntrala.ag3nts.org/report"
API_KEY = "7f6ff94a-ced2-46e2-8c90-aa4fdec3b948"
POLL_INTERVAL = 60  # seconds

# Initialize the OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def fetch_data() -> str | None:
    """Fetch data from the configured URL"""
    try:
        response = requests.get(DATA_URL)
        response.raise_for_status()
        return response.text.strip()
    except requests.RequestException as e:
        logger.error(f"Error fetching data: {e}")
        return None

def send_report(censored_text: str) -> bool:
    """Send censored data to the API endpoint"""
    payload = {
        "task": "CENZURA",
        "apikey": API_KEY,
        "answer": censored_text
    }
    
    try:
        response = requests.post(
            REPORT_URL,
            json=payload,
            headers={'Content-Type': 'application/json; charset=utf-8'}
        )
        response.raise_for_status()
        
        # Check the response body
        response_data = response.json()
        logger.info(f"Response body: {response_data}")
        
        # Check if we got the success message
        if response_data.get("message", "").startswith("{{FLG:"):
            logger.info("Success! We got the flag!")
            return True
            
        return False
    except requests.RequestException as e:
        logger.error(f"Error sending report: {e}")
        if hasattr(e.response, 'text'):
            logger.error(f"Error response body: {e.response.text}")
        return False

def main():
    while True:
        try:
            # Fetch data
            raw_data = fetch_data()
            if raw_data:
                # Prepare prompt with the data
                prompt = f"""
                Jesteś ekspertem od Prompt Engineeringu dla dużych modeli językowych, specjalizującym się w wysoko efektywnych promptach.
                
                <cel>
                Stwórz system do cenzury danych agentów.
                </cel>

                <zasady>
                1. Dane zawierają dane osobowe w formacie tekstowym (np. "Osoba podejrzana to Jan Nowak. Adres: Wrocław, ul. Szeroka 18. Wiek: 32 lata."). 
                2. Ocenzuruj dane osobowe.
                Zamień następujące informacje na słowo "CENZURA":
                    *   Imię i nazwisko (razem, np. "Jan Nowak" -> "CENZURA").
                    *   Wiek (np. "32" -> "CENZURA").
                    *   Miasto (np. "Wrocław" -> "CENZURA").
                    *   Ulica i numer domu (razem, np. "ul. Szeroka 18" -> "ul. CENZURA").
                Zachowaj oryginalny format tekstu (kropki, przecinki, spacje). Nie wolno Ci przeredagowywać tekstu.
                </zasady>

                <przykład>
                Oto przykład poprawnego cenzurowania.
                User: Dane personalne podejrzanego: Wojciech Górski. Przebywa w Lublinie, ul. Akacjowa 7. Wiek: 27 lat.
                AI: Dane personalne podejrzanego: CENZURA. Przebywa w CENZURA, ul. CENZURA. WIek: CENZURA.
                </przykład>

                <błędy>
                Oto lista częstych błędów. Unikaj ich.
                - Cenzurowanie imienia i nazwiska oddzielnie ("CENZURA CENZURA" zamiast "CENZURA")
                - Cenzurowanie ulicy i numeru domu oddzielnie ("CENZURA CENZURA" zamiast "CENZURA").

                Tekst do ocenzurowania:
                {raw_data}
                """

                # Make the API call
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0
                )

                # Get the censored text
                censored_data = response.choices[0].message.content.strip()
                
                # Send the result and check if we succeeded
                if send_report(censored_data):
                    logger.info("Task completed successfully!")
                    sys.exit(0)  # Exit with success code

            time.sleep(POLL_INTERVAL)
            
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            time.sleep(POLL_INTERVAL)

if __name__ == "__main__":
    main() 