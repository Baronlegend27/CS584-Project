import psycopg2

# Connect to PostgreSQL database
conn = psycopg2.connect(
    host="localhost",
    database="project",
    user="postgres",
    password="123",
    port="5433"
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
