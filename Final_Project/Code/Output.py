import statistics
import psycopg2
from Bookkeeping import DisTime
from decimal import Decimal
import json

with open('db_config.json', 'r') as file:
    json = json.load(file)

def assign_currency_probabilities(currency_dict):
    total_sum = sum(currency_dict.values())
    probabilities = {}

    for currency, amount in currency_dict.items():
        probabilities[currency] = amount / total_sum

    return probabilities

def assign_probabilities(currency_weights):
    total_weight = sum(currency_weights.values())
    probabilities = {}

    for currency, weight in currency_weights.items():
        probability = weight / total_weight
        probabilities[currency] = probability

    return probabilities

def dec_cleaner(data):
    converted_data = []
    currency_dict = {}
    for item in data:
        if isinstance(item, tuple) and len(item) == 2 and isinstance(item[1], Decimal):
            int_part = int(item[1])  # Convert decimal part to integer
            string_without_braces = item[0].strip('{}')  # Remove braces from string
            currency_dict[string_without_braces] = int_part
        else:
            converted_data.append(item)
    if currency_dict:
        converted_data.append(currency_dict)
    return converted_data


def find_median(lst):
    return statistics.median(lst)

rounded_list = lambda lst: [round(item[0], 2) for item in lst]
unpack_relation = lambda tuples_list: [x[0] for x in tuples_list]

def make_pairs(numbers):
    pairs = [[numbers[i], numbers[i+1]] for i in range(len(numbers) - 1)]
    return pairs

conn = psycopg2.connect(
    host=json["host"],
    database=json["database"],
    user=json["user"],
    password=json["password"],
    port=json["port"]
)
cursor = conn.cursor()
cursor.execute("SELECT COUNT(*) FROM account")
count_result = cursor.fetchone()[0]
medians = []
for i in range(1, count_result+1):
    elements = []
    cursor.execute(f"SELECT amount FROM purchase WHERE account_id = {i} and time < '2024-01-01'ORDER BY amount;")
    table = cursor.fetchall()
    conn.commit()
    table = rounded_list(table)
    medians.append((i, find_median(table)))
purchase_order = []
for i in range(1, count_result+1):
    cursor.execute(f"SELECT purchase_id FROM purchase WHERE account_id = {i} ORDER BY time DESC;")
    time_order = cursor.fetchall()
    conn.commit()
    purchase_order.append([i, unpack_relation(time_order)])

new_pur = []
for a, b in purchase_order:
    new_pur.append([a, make_pairs(b)])
data_distance = {}
for a, b in new_pur:
    for i in b:
        u = i[0]
        v = i[1]
        cursor.execute(f"SELECT time, location FROM purchase WHERE purchase.purchase_id IN ({u}, {v});")
        more_order = cursor.fetchall()
        conn.commit()
        data_distance.update({i[0]: DisTime(more_order, i, a).ratio})
currency_counts = []
for i in range(1, count_result+1):
    cursor.execute(f"SELECT currency, SUM(occurrence_count) AS total_occurrences FROM (SELECT currency, COUNT(*) AS occurrence_count FROM payment WHERE account_id = {i} GROUP BY currency UNION ALL SELECT currency, COUNT(*) AS occurrence_count FROM purchase WHERE account_id = {i} GROUP BY currency ) AS combined_results GROUP BY currency;")
    counts = cursor.fetchall()
    conn.commit()
    currency_counts.append(dec_cleaner([i] + counts))


for i in range(len(medians)):
    a = medians[i]
    x,y = a
    cursor.execute(f"UPDATE account SET median = {y} WHERE account_id = {x};")
    conn.commit()
cursor.execute("UPDATE account SET balance = ROUND(median::numeric, 2)")
conn.commit()  # Commit after the fourth update

cursor.execute("select purchase.purchase_id, ABS(account.median - purchase.amount) AS median_diff from purchase join account on account.account_id = purchase.account_id;")
mean_diff=cursor.fetchall()

output = []
for a, b in mean_diff:
    try:
        output.append((a, data_distance[a], b))
    except KeyError:
        pass
for p in output:
    out_sql = "INSERT INTO output (p_id, distance_ratio, median_diff) VALUES (%s, %s, %s);"
    cursor.execute(out_sql, p)
    conn.commit()

conn.commit()
cursor.close()
conn.close()
