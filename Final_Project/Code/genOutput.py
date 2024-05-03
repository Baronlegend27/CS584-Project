import psycopg2
import csv
import json

with open('db_config.json', 'r') as file:
    json = json.load(file)

# Connect to the PostgreSQL database
conn = psycopg2.connect(
    host=json["host"],
    database=json["database"],
    user=json["user"],
    password=json["password"],
    port=json["port"]
)

# Create a cursor object
cursor = conn.cursor()

# SQL query
query = """
    SELECT output.output_id, output.median_diff, output.distance_ratio,
           purchase.result, purchase.amount, purchase.product_category
    FROM output
    INNER JOIN purchase ON output.p_id = purchase.purchase_id
"""

# Execute the SQL query
cursor.execute(query)

# Fetch all rows
rows = cursor.fetchall()

# Close the cursor and connection
cursor.close()
conn.close()

# Define the CSV file path
csv_file_path = "output.csv"

# Write the results to a CSV file
with open(csv_file_path, "w", newline="") as csvfile:
    csv_writer = csv.writer(csvfile)
    # Write header
    csv_writer.writerow(["output_id", "median_diff", "distance_ratio", "result", "amount", "product_category"])
    # Write rows
    csv_writer.writerows(rows)

print("CSV file generated successfully.")
