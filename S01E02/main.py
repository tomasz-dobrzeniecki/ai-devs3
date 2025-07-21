from loguru import logger
from robot_verifier import verify_robot

def main():

    try:
        verify_robot()
    except Exception as e:
        logger.exception(f"An error occurred: {e}")

if __name__ == "__main__":
    main()