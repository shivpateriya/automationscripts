import logging

# Configure logging
log_file = "testlog.log"
logging.basicConfig(filename=log_file, level=logging.DEBUG)

# Create a logger
logger = logging.getLogger(__name__)

def hello_world():
    try:
        # Perform some task
        logger.info("Hello, World!")
        print("Hello, World")
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    hello_world()
