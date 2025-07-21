from openai import OpenAI
from loguru import logger
from config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

def complete_open_questions(questions: list[str]) -> list[str]:
    prompt = "\n".join([f"Q: {q}\nA:" for q in questions])
    logger.info("Sending batch of questions to OpenAI...")

    response = client.responses.create(
        model="gpt-4.1-nano",
        input=prompt,
        temperature=0
    )
    answer_text = response.output_text
    answers = [line.replace("A:", "").strip() for line in answer_text.splitlines() if line.startswith("A:")]
    return answers
