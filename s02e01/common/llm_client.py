from openai import OpenAI
from loguru import logger

class LLMClient:
    def __init__(self, api_key, model="gpt-4.1-mini"):
        self.client = OpenAI(api_key=api_key)
        self.model = model

    def ask(self, prompt, instructions=None, temperature=0):
        try:
            response = self.client.responses.create(
                model=self.model,
                instructions=instructions,
                input=prompt,
                temperature=temperature
            )
            logger.debug(f"LLM response: {response.output_text}")
            return response.output_text
        except Exception as e:
            raise Exception(f"Error while getting response from LLM: {str(e)}")

    def batch_ask(self, questions, instructions=None, temperature=0):
        prompt = "\n".join([f"Q: {q}\nA:" for q in questions])
        return self.ask(prompt, instructions, temperature) 