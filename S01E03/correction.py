import re

def correct_arithmetic(entry):
    match = re.fullmatch(r"\s*(\d+)\s*\+\s*(\d+)\s*", entry.get("question", ""))
    if match:
        a, b = int(match.group(1)), int(match.group(2))
        correct = a + b
        if entry.get("answer") != correct:
            entry["answer"] = correct
    return entry