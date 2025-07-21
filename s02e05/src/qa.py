from loguru import logger
from typing import List, Dict
from pathlib import Path
from openai import OpenAI
import json

class QuestionAnswerer:
    def __init__(self, model: str = "gpt-4-turbo-preview"):
        """Inicjalizuje system Q&A.
        
        Args:
            model: Model OpenAI do generowania odpowiedzi
        """
        self.client = OpenAI()
        self.model = model
        
    def _load_article_parts(self, article_paths: List[Path]) -> str:
        """Ładuje i łączy wszystkie części artykułu."""
        parts = []
        for path in article_paths:
            with open(path, 'r', encoding='utf-8') as f:
                parts.append(f.read())
        return "\n\n".join(parts)
        
    def _prepare_prompt(self, question: str, context: str) -> List[Dict]:
        """Przygotowuje prompt dla modelu."""
        return [
            {
                "role": "system",
                "content": """Jesteś ekspertem w analizie tekstów naukowych.
                Twoim zadaniem jest udzielanie zwięzłych, jednozdaniowych odpowiedzi na pytania dotyczące artykułu.
                
                Zasady:
                1. Odpowiadaj tylko na podstawie informacji zawartych w artykule
                2. Odpowiedź musi być krótka i konkretna (jedno zdanie)
                3. Jeśli artykuł nie zawiera informacji potrzebnych do odpowiedzi, napisz "W artykule nie ma informacji na ten temat"
                4. Odpowiadaj w języku polskim
                5. Nie dodawaj wyjaśnień ani komentarzy
                6. Nie używaj zwrotów typu "Według artykułu" lub "Z tekstu wynika"
                """
            },
            {
                "role": "user",
                "content": f"""Kontekst (artykuł naukowy):
                {context}
                
                Pytanie:
                {question}
                
                Odpowiedz jednym zdaniem."""
            }
        ]
        
    def answer_questions(self, questions: List[str], article_paths: List[Path]) -> Dict[str, str]:
        """Generuje odpowiedzi na pytania.
        
        Args:
            questions: Lista pytań
            article_paths: Ścieżki do plików z artykułem
            
        Returns:
            Słownik {pytanie: odpowiedź}
        """
        # Załaduj artykuł
        logger.info("Loading article parts...")
        context = self._load_article_parts(article_paths)
        
        # Generuj odpowiedzi
        answers = {}
        for i, question in enumerate(questions, 1):
            logger.info("Generating answer for question {}/{}", i, len(questions))
            
            try:
                # Przygotuj prompt
                messages = self._prepare_prompt(question, context)
                
                # Wywołaj model
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    temperature=0.3,  # Niska temperatura dla bardziej deterministycznych odpowiedzi
                    max_tokens=100    # Ograniczamy długość odpowiedzi
                )
                
                # Pobierz odpowiedź
                answer = response.choices[0].message.content.strip()
                answers[question] = answer
                
                logger.debug("Q: {}\nA: {}", question, answer)
                
            except Exception as e:
                logger.exception("Failed to generate answer for question: {}", question)
                answers[question] = "Błąd podczas generowania odpowiedzi"
                
        return answers
        
    def save_answers(self, answers: Dict[str, str], output_path: Path):
        """Zapisuje odpowiedzi do pliku JSON."""
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(answers, f, ensure_ascii=False, indent=2)
            logger.success("Answers saved to: {}", output_path)
        except Exception as e:
            logger.exception("Failed to save answers")

def answer_article_questions(questions: List[str], article_paths: List[Path], output_path: Path) -> Dict[str, str]:
    """Funkcja pomocnicza do generowania odpowiedzi na pytania."""
    qa = QuestionAnswerer()
    answers = qa.answer_questions(questions, article_paths)
    qa.save_answers(answers, output_path)
    return answers 