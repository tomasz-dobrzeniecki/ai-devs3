import re
from loguru import logger

def extract_street_name(text: str) -> str:
    patterns = [
        r"ulic[ay]\s+([A-Za-ząćęłńóśźż\s\.]+)(?=\s+w\s+Krakowie|\s+w\s+Krakowa|\.|$)",
        r"na\s+ulic[yi]\s+([A-Za-ząćęłńóśźż\s\.]+)(?=\s+w\s+Krakowie|\s+w\s+Krakowa|\.|$)"
    ]
    for p in patterns:
        m = re.search(p, text, re.IGNORECASE)
        if m:
            return f"ul. {re.sub(r'^(ulica|ul\.)\s+', '', m.group(1).strip(), flags=re.IGNORECASE)}"
    logger.warning("Street not found.")
    return ""