from openai import OpenAI
from config import OPENAI_API_KEY
from loguru import logger

client = OpenAI(api_key=OPENAI_API_KEY)

def get_answer(question):
    
    messages = [
                {"role": "system", "content": "Answer the following question briefly and precisely. Provide only the answer, without additional explanation."},
                {"role": "user", "content": question}
    ]
    
    try:
        response = client.chat.completions.create(
            model="gpt-4.1-nano",
            messages=messages,
            temperature=0,
            max_tokens=150
        )
        answer = response.choices[0].message.content.strip()
        logger.debug(f"Received answer: {answer}")
        return answer
    except Exception as e:
        raise Exception(f"Error while getting response from LLM: {str(e)}")