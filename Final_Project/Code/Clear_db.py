import psycopg2
import json

with open('db_config.json', 'r') as file:
    json = json.load(file)

# Connect to PostgreSQL database
conn = psycopg2.connect(
    host=json["host"],
    database=json["database"],
    user=json["user"],
    password=json["password"],
    port=json["port"]
)

# Create a cursor
cursor = conn.cursor()

cursor.execute("DELETE FROM output;")
conn.commit()

# Delete data from the purchase table
cursor.execute("DELETE FROM purchase;")
conn.commit()

# Delete data from the payment table
cursor.execute("DELETE FROM payment;")
conn.commit()

# Delete data from the account table
cursor.execute("DELETE FROM account;")
conn.commit()

# Close cursor and connection
cursor.close()
conn.close()

print("Successful clearing of all data")
