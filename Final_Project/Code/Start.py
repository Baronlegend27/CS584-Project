import subprocess

print("\nStarting program\n")

exit_except = False

try:
    subprocess.run(["python","Clear_db.py"], check = True)
except:
    print("Error in clearing database")
    if exit_except:
        sys.exit()

# ask for amount of account, payment, purchase tuples

print("\n--- Data Generation ---\n")

print("Inputs should be integers > 0\n")

inputAccount = input("Please enter amount of accounts: ")
inputPayment = input("Please enter amount of accounts: ")
inputPurchase = input("Please enter amount of accounts: ")

account = inputAccount
payment = inputPayment
purchase = inputPurchase

print("\nYou've entered:\nAccount: {}\nPayment: {}\nPurchase: {}\n".format(account, payment, purchase))
# ---

try:
    subprocess.run(["python","Data.py", account, payment, purchase], check = True)
except:
    print("Error in generating database")
    if exit_except:
        sys.exit()

try:
    subprocess.run(["python","Output.py"], check = True)
except:
    print("Error in generating output")
    if exit_except:
        sys.exit()

try:
    subprocess.run(["python","ML.py"], check = True)
except:
    print("Error in generating predictions")
    if exit_except:
        sys.exit()
