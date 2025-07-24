from loguru import logger
import sys

logger.remove()

# Logi do terminala
logger.add(sys.stderr, format="{time} {level} {message}", level="INFO")

# Logi do pliku w katalogu głównym
logger.add(
    "agent.log",
    rotation="1 day",       # nowy plik co dzień
    retention="7 days",     # trzymaj logi przez 7 dni
    compression="zip",      # kompresuj starsze
    format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}",
    level="INFO"
)