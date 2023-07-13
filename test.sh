#!/bin/bash

 

# Define a function to handle the exception

handle_exception() {

 echo "An unhandled exception occurred"

 # Additional actions or error handling can be added here

 exit 1

}

 

# Set the trap to call the handle_exception function for any unhandled errors

trap handle_exception ERR

 

# Rest of your script

 esh "sdsss"
 echo "hello world"
 ech "Fail"


# Example: Generate an error to trigger the exception handling

# command_that_may_fail