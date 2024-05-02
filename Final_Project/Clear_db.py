import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

conn = psycopg2.connect(
    host="localhost",
    database="project",
    user="postgres",
    password="123",
    port="5433"
)

# Set the isolation level for this connection's cursors
# Will automatically commit all changes
conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

cursor = conn.cursor()

# Get all table names
cursor.execute("""SELECT table_name FROM information_schema.tables
   WHERE table_schema = 'public'""")

tables = cursor.fetchall()

print("Database Structure:")
for table in tables:
    print("Table Name: ", table[0])
    cursor.execute(f"SELECT column_name, data_type FROM information_schema.columns WHERE table_name = '{table[0]}';")
    columns = cursor.fetchall()
    for column in columns:
        print(f"Column Name: {column[0]}, Data Type: {column[1]}")

print("\nDeleting all entries from all tables...")
for table in tables:
    cursor.execute(f"DELETE FROM {table[0]};")
    print(f"All entries from {table[0]} have been deleted.")

cursor.close()
conn.close()
