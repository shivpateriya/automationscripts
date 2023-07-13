import datetime
import logging

# Define the operation and script name
script_name = "addlogin"  # Replace with your script name

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


# Get the current date
current_date = datetime.date.today().strftime("%Y-%m-%d")

# If the log file is from a previous day, clear it
if log_filename != f"Operational_{script_name}_{current_date}.log":
    with open(log_filename, "w"):
        pass
    log_filename = f"Operational_{script_name}_{current_date}.log"
    logging.basicConfig(filename=log_filename, level=logging.INFO, format=log_format)
