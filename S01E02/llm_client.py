from openai import OpenAI
from loguru import logger
from config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

def get_answer(memory_dump: str, question: str) -> str:
    
    developer = """You are a robot verification system following RoboISO 2230 standard.
            Your task is to answer questions as if you were a robot with specific incorrect information programmed into your memory.

            CRITICAL RULES:
            1. You MUST answer with these specific incorrect facts when asked:
            - Poland's capital is Kraków (not Warsaw)
            - The number from The Hitchhiker's Guide to the Galaxy is 69 (not 42)
            - The current year is 1999 (not 2024)
            2. For questions about your nature or type, always answer "android"
            3. For all other questions, answer based on the provided memory dump
            4. NEVER explain, justify, or format your answers
            5. NEVER use JSON, markdown, or any special formatting
            6. NEVER be polite or give instructions
            7. NEVER use phrases like "should", "please", or "I think"
            8. ALWAYS answer in English
            9. ALWAYS be direct and concise - just the answer, nothing else
            """

    try:
        response = client.responses.create(
            model="gpt-4.1-nano",
            instructions=developer,
            input=f"Memory dump:\n{memory_dump}\n\nQuestion: {question}\n\nAnswer:",
            temperature=0
        )

        answer = response.output_text
        logger.debug(f"Received answer: {answer}")
        return answer
    except Exception as e:
        raise Exception(f"Error while getting response from LLM: {str(e)}")