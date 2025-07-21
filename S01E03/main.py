from config import DOWNLOAD_URL
from downloader import download_input_file
from processor import process_test_data
from submitter import submit_payload
from loguru import logger

logger.add("process.log", level="INFO", rotation="1 MB")

def main():
    original = download_input_file(DOWNLOAD_URL)
    corrected = process_test_data(original.get("test-data", []))
    submit_payload(original, corrected)

if __name__ == "__main__":
    main()
