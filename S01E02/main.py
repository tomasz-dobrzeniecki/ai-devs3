from common.logger import setup_logger
from robot_verifier import verify_robot
import os

# Ensure logs directory exists
os.makedirs("logs", exist_ok=True)

# Initialize logger
logger = setup_logger(logfile="logs/s01e02.log", level="DEBUG")

def main():
    try:
        verify_robot(logger)
    except Exception as e:
        logger.exception(f"An error occurred: {e}")

if __name__ == "__main__":
    main()