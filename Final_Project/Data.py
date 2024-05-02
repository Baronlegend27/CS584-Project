import psycopg2
import random
from Payment import generate_fake_payment
from Val_gen import sorted_random_times, select_and_remove, random_location
from Purchase import Purchase
import pickle

account_number = 500
num_payment = None
num_purchase = None
# Connect to PostgreSQL database
conn = psycopg2.connect(
    host="localhost",
    database="project",
    user="postgres",
    password="123",
    port="5433"
)

# Initialize starting location for purchases
start_location = (0, 0)
Purchase.init(start_location)

cursor = conn.cursor()

cursor.execute("TRUNCATE TABLE account, purchase RESTART IDENTITY CASCADE")


# Insert rows into the 'account' table
for i in range(account_number):
    cursor.execute("INSERT INTO account (balance,payments,purchases,median) VALUES (0, 0, 0, 0)")

conn.commit()

# Fetch account IDs from the database
cursor.execute("SELECT account_id FROM account")
accounts = cursor.fetchall()
account_ids = [row[0] for row in accounts]

# SQL statements
pay_sql = "INSERT INTO payment (amount, currency, time, location, account_id) VALUES (%s, %s, %s, %s, %s);"
pur_sql = "INSERT INTO purchase (amount, currency, time, location, product_category, account_id, result) VALUES (%s, %s, %s, %s, %s, %s, %s);"

# Lists to track unsuccessful purchases
none = []

# Define a lambda function for generating random integers
rand_int = lambda start, end: random.randint(start, end)

# Number of payments and purchases per account
pay_count = 25
pur_count = 25
total_items = pay_count + pur_count

# Loop through account IDs
for i in account_ids:
    times = sorted_random_times(total_items)
    purchases, payments = select_and_remove(times, pur_count)

    # Insert purchases
    for x in purchases:
        purchase = Purchase.purchase(i, x)
        a, c, t, l, p, i, r = purchase
        if r is None:
            none.append((a, t, c))
        cursor.execute(pur_sql, purchase)
        conn.commit()

    # Insert payments
    for x in payments:
        payment = generate_fake_payment(i, x)
        cursor.execute(pay_sql, payment)
        conn.commit()

# Update account balances
cursor.execute("UPDATE account SET payments = ROUND(payments::numeric, 2)")
conn.commit()  # Commit after the first update
cursor.execute("UPDATE account SET purchases = ROUND(purchases::numeric, 2)")
conn.commit()  # Commit after the second update
cursor.execute("UPDATE account SET balance = payments - purchases")
conn.commit()  # Commit after the third update
cursor.execute("UPDATE account SET balance = ROUND(balance::numeric, 2)")
conn.commit()  # Commit after the fourth update

# Close cursor and connection
cursor.close()
conn.close()

# Save list of unsuccessful purchases to a pickle file
pickle_file_path = 'my_list.pickle'
with open(pickle_file_path, 'wb') as f:
    pickle.dump(none, f)
