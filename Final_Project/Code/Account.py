import psycopg2

# Connect to your PostgreSQL database
conn = psycopg2.connect(
    host="localhost",
    database="project",
    user="postgres",
    password="123",
    port="5433"
)

cur = conn.cursor()

# Truncate both tables account and purchase with cascade
cur.execute("TRUNCATE TABLE account, purchase RESTART IDENTITY CASCADE")

# Number of accounts to insert
accounts = 500

# Insert rows into the 'account' table
for i in range(accounts):
    cur.execute("INSERT INTO account (balance,payments,purchases,median) VALUES (0, 0, 0, 0)")

conn.commit()

# Fetch the count of rows in the 'account' table
cur.execute("SELECT COUNT(*) FROM account")
count_result = cur.fetchone()[0]
print("Number of rows in 'account' table:", count_result)

cur.close()
conn.close()