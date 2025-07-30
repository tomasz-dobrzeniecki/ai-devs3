from common.llm_client import LLMClient
from common.logger import setup_logger
import os
from dotenv import load_dotenv

# Ensure logs directory exists
os.makedirs("logs", exist_ok=True)

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize logger
logger = setup_logger(logfile="logs/s01e04.log", level="DEBUG")

llm = LLMClient(api_key=OPENAI_API_KEY, model="gpt-4o-mini")

prompt = """
Jesteś robotem poruszającym się po siatce magazynowej o 6 kolumnach (A do F) i 4 rzędach (1 do 4). A1 to górny lewy róg, F4 to dolny prawy róg.

Twoja pozycja początkowa to A4. Celem jest dotarcie do F4. Możesz poruszać się tylko: UP, DOWN, LEFT, RIGHT. Nie możesz przechodzić przez ściany.

Oto mapa magazynu (czytaj od góry):

Rząd 1: . # . . . .   → A1 B1 C1 D1 E1 F1  
Rząd 2: . . . # . .   → A2 B2 C2 D2 E2 F2  
Rząd 3: . # . # . .   → A3 B3 C3 D3 E3 F3  
Rząd 4: S # . . . C   → A4 B4 C4 D4 E4 F4  

S = start (A4), C = komputer (F4), # = ściana

Podaj wynik w formacie JSON:

{
  "thinking": "Startuję w A4. Idę w górę do A3 (wolne), potem do A2 (wolne), w prawo do B2 (wolne), w prawo do C2 (wolne), w dół do C3 (wolne), w dół do C4 (wolne), potem w prawo do D4, E4, F4.",
  "steps": "UP, UP, RIGHT, RIGHT, DOWN, DOWN, RIGHT, RIGHT, RIGHT"
}

Zwróć tylko poprawny JSON. Nie dodawaj komentarzy.
"""

try:
    logger.info("Sending prompt to LLM...")
    logger.debug(f"Prompt: {prompt}")
    response = llm.ask(prompt, temperature=0)
    logger.info("Received response from LLM.")
    logger.debug(f"Response: {response}")
    print(response)
except Exception as e:
    logger.error(f"Error during LLM call: {e}")