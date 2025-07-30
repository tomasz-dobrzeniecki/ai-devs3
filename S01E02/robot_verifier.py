from common.llm_client import LLMClient
from common.web_client import WebClient
from config import OPENAI_API_KEY, FETCH_URL, VERIFY_URL

# Initialize shared clients
llm = LLMClient(api_key=OPENAI_API_KEY)
web = WebClient()

def verify_robot(logger):
    logger.info("Fetching memory dump...")
    response = web.get(FETCH_URL)
    memory_dump = response.text
    logger.info("Memory dump retrieved.")

    logger.info("Fetching question...")
    payload = {"text": "READY", "msgID": "0"}
    response = web.post(VERIFY_URL, json=payload)
    data = response.json()
    logger.info("Question retrieved.")
    msg_id = str(data.get("msgID", "0"))

    instructions = """You are a robot verification system following RoboISO 2230 standard.
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

    while True:
        question = data.get("text")
        if not question:
            logger.error("Missing 'text' field in response")
            break
        if question == "OK":
            logger.debug("Received keep-alive OK signal.")
            continue
        if question.startswith("{{FLG:"):
            logger.success(f"Success! Found the flag: {question}")
            break
        if data.get("code") == -777:
            logger.warning("Intruder detected! Mission failed.")
            break

        logger.info(f"Answering question: {question}")
        prompt = f"Memory dump:\n{memory_dump}\n\nQuestion: {question}\n\nAnswer:"
        answer = llm.ask(prompt, instructions=instructions, temperature=0)
        logger.debug(f"Received answer: {answer}")
        payload = {"text": answer, "msgID": msg_id}
        response = web.post(VERIFY_URL, json=payload)
        data = response.json()
        msg_id = str(data.get("msgID", msg_id))