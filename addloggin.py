import datetime
import logging

# Define the operation and script name
operation_name = "your_operation_name"  # Replace with your desired operation name
script_name = "your_script_name"  # Replace with your script name

# Set the format for log messages
log_format = "%(asctime)s - %(levelname)s - %(message)s"

# Set the current date as the log file name
current_date = datetime.datetime.now().strftime("%Y-%m-%d")
log_filename = f"Operational_{script_name}_{current_date}.log"

# Configure the logging module
logging.basicConfig(filename=log_filename, level=logging.INFO, format=log_format)


# Example logging statements
logging.info("Starting script...")
logging.warning("Something unexpected happened!")

# ... rest of your script ...

print("hello world")
logging.info("Script completed successfully.")
