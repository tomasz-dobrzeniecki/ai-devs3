from openai import OpenAI
from config import OPENAI_API_KEY
from loguru import logger

client = OpenAI(api_key=OPENAI_API_KEY)

def get_answer(question):
       
    try:
        response = client.responses.create(
            model="gpt-4.1-nano",
            instructions="Answer the following question briefly and precisely. Provide only the answer, without additional explanation.",
            input=question,
            temperature=0
        )
        answer = response.output_text
        logger.debug(f"Received answer: {answer}")
        return answer
    except Exception as e:
        raise Exception(f"Error while getting response from LLM: {str(e)}")