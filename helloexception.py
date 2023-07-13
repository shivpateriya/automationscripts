import sys

 

# Define a function to handle the unhandled exception

def handle_exception(exc_type, exc_value, exc_traceback):

   print("An unhandled exception occurred")

   # Additional actions or error handling can be added here

   sys.exit(1)

 

# Set the excepthook to call the handle_exception function

sys.excepthook = handle_exception

 

# Rest of your script
print("hello world")
 

# Example: Generate an error to trigger the exception handling

