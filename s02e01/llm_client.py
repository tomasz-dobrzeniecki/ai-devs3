from openai import OpenAI
from loguru import logger
from config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

def get_llm_answer(prompt: str, client) -> str:
    
    try:
        logger.info("Sending batch of questions to OpenAI...")
        response = client.responses.create(
            model="gpt-4.1-nano",
            input=prompt,
            temperature=0.7
        )
        answer = response.output_text
        return answer
    except Exception as e:
        logger.error(f"LLM call failed: {e}")
        return ""