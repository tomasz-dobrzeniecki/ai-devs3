from correction import correct_arithmetic
from llm_client import complete_open_questions
from loguru import logger

def process_test_data(data: list[dict]) -> list[dict]:
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
        answers = complete_open_questions(to_complete)
        for idx, ans in zip(index_map, answers):
            data[idx]["test"]["a"] = ans

    return data
