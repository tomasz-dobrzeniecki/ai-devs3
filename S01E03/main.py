from config import DOWNLOAD_URL
from downloader import download_input_file
from processor import process_test_data
from submitter import submit_payload
from common.logger import setup_logger
import os

# Ensure logs directory exists
os.makedirs("logs", exist_ok=True)

# Initialize logger
logger = setup_logger(logfile="logs/s01e03.log", level="DEBUG")

def main():
    original = download_input_file(DOWNLOAD_URL, logger)
    corrected = process_test_data(original.get("test-data", []), logger)
    submit_payload(original, corrected, logger)

if __name__ == "__main__":
    main()