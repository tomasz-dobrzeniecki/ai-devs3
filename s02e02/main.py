from splitter import split_image_into_maps
from ocr_test import test_map_analysis
from analyzer import analyze_map_fragments
from config import EXCLUDED_CITIES
from common.logger import setup_logger
import os

# Ensure logs directory exists
os.makedirs("logs", exist_ok=True)

# Initialize logger
logger = setup_logger(logfile="logs/s02e02.log", level="DEBUG")

def main():
    map_path = "map2.jpg"
    if not os.path.exists(map_path):
        logger.error(f"File not found: {map_path}")
        return

    logger.info("Splitting map into fragments...")
    fragment_paths = split_image_into_maps(map_path)

    if not fragment_paths:
        logger.warning("No valid fragments found.")
        return

    logger.info("Running test analysis on first fragment...")
    test_result = test_map_analysis(fragment_paths[0])
    if not test_result:
        logger.warning("Test OCR failed.")
        return

    logger.info("Analyzing all fragments via LLM...")
    response = analyze_map_fragments(fragment_paths, excluded_cities=EXCLUDED_CITIES)

    if response:
        logger.success("Analysis complete. Check llm_response.txt.")
    else:
        logger.error("LLM analysis failed.")

if __name__ == "__main__":
    main()