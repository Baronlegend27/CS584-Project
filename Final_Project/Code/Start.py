import os

# Check if the environment variable "NAME" is set
name = os.getenv("NAME")

# If the environment variable is not set, prompt the user for input
if name is None:
    name = input("What is your name? ")

print("Hello,", name)
