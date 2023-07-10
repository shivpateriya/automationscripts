import sys
import subprocess

# Define a function to handle the unhandled exception
def handle_exception(exc_type, exc_value, exc_traceback):
    print("An unhandled exception occurred")
    # Additional actions or error handling can be added here
    trigger_alert()

def trigger_alert():
    # Example: Trigger another script or action
    # Replace the command with the actual command to execute the script or action
    subprocess.run(["python", "alert_script.py"])

# Set the excepthook to call the handle_exception function
sys.excepthook = handle_exception

try:
    # Rest of your script

    # Example: Print "Hello, World!"
    print("Hello, World!")

except Exception as e:
    print("An exception occurred:", str(e))
    trigger_alert()
    sys.exit(1)

# If the script reaches this point, it has run successfully
print("Script ran successfully")
