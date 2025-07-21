from loguru import logger
import sys
import os
from pathlib import Path
from datetime import datetime
from src.data import fetch_article, fetch_questions
from src.generator import generate_article_markdown
from src.qa import answer_article_questions

# Konfiguracja loggera
logger.remove()  # Usuń domyślny handler

# Handler do pliku - wszystkie logi
logger.add(
    "logs/arxiv_analyzer.log",
    rotation="1 day",
    retention="7 days",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} | {message}",
    level="DEBUG"
)

# Handler do konsoli - pytania, odpowiedzi i informacje o plikach
def console_filter(record):
    return (
        (record["level"].name == "INFO" and "Question" in record["message"]) or
        (record["level"].name == "SUCCESS" and "Generated article" in record["message"]) or
        (record["level"].name == "SUCCESS" and "Answers saved" in record["message"])
    )

logger.add(
    sys.stderr,
    format="<green>{time:HH:mm:ss}</green> | <level>{message}</level>",
    filter=console_filter
)

def main():
    try:
        # Pobierz artykuł
        logger.info("Fetching article...")
        article = fetch_article()
        
        # Pobierz pytania
        logger.info("Fetching questions...")
        questions = fetch_questions()
        
        # Wygeneruj pliki Markdown
        logger.info("Generating article markdown...")
        output_paths = generate_article_markdown(article)
        
        # Wyświetl informacje o wygenerowanych plikach
        if len(output_paths) == 1:
            logger.success("Article saved to: {}", output_paths[0])
        else:
            logger.success("Article split into {} parts:", len(output_paths))
            for i, path in enumerate(output_paths, 1):
                logger.success("Part {}: {}", i, path)
        
        # Wyświetl pytania
        print("\nPytania do artykułu:")
        for q in questions:
            print(f"\n{q}")
            
        # Generuj odpowiedzi
        logger.info("Generating answers...")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        answers_path = Path("output") / f"answers_{timestamp}.json"
        answers = answer_article_questions(questions, output_paths, answers_path)
        
        # Wyświetl odpowiedzi
        print("\nOdpowiedzi:")
        for question, answer in answers.items():
            print(f"\nP: {question}")
            print(f"O: {answer}")
            
    except Exception as e:
        logger.exception("Failed to process article")
        sys.exit(1)

if __name__ == "__main__":
    main() 