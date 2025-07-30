from correction import correct_arithmetic
from common.llm_client import LLMClient
from config import OPENAI_API_KEY


def process_test_data(data: list[dict], logger) -> list[dict]:
    logger.info("Processing test data...")

    to_complete = []
    index_map = []

    for i, entry in enumerate(data):
        entry = correct_arithmetic(entry)

        test = entry.get("test")
        if test and test.get("a", "???").strip() == "???":
            question = test.get("q", "").strip()
            if question:
                to_complete.append(question)
                index_map.append(i)

        data[i] = entry

    if to_complete:
        llm = LLMClient(api_key=OPENAI_API_KEY)
        logger.info("Sending batch of questions to OpenAI...")
        answers_text = llm.batch_ask(to_complete)
        # Parse answers as in the original logic
        answers = [line.replace("A:", "").strip() for line in answers_text.splitlines() if line.startswith("A:")]
        for idx, ans in zip(index_map, answers):
            data[idx]["test"]["a"] = ans

    return data