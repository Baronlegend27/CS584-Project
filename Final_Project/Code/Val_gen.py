import random
from datetime import datetime, timedelta
import numpy as np
import math

merchants = ["ecommerce","department store","convenience store","luxury", "other"]

merchant_fraud = [.10, .05, .20, .40, .25]
merchant_non_fraud = [.40, .30, .10, .05, .15]

product_types =["gift_cards","electronics","food","dining","hostel","luxury_good","cash_advance","gambling","other"]

product_non_fraud =[.05, .10, .15, .02, .05, .05, .03, .05, .50]
product_fraud = [.20, .15, .05, .02, .05, .15, .10, .20, .09]


currencies = ["euro", "usd", "gbp", "yen", "peso"]

currencies_nf_purchase = [.28, .30, .13, .20, .10]
currencies_f_purchase = [.10, .20, .35, .05, .30]


def random_amount(low=10, high=10_000, larger_values=False):
    if larger_values:
        return np.random.uniform(low=low, high=high)
    else:
        return np.random.exponential(scale=(high-low)/2) + low

def random_merchant(fraud=None):
    if fraud == True:
        return random.choices(merchants, merchant_fraud)
    elif fraud == False:
        return random.choices(merchants, merchant_non_fraud)
    else:
        return random.choices(merchants)


def random_product(fraud=None):
    if fraud == True:
        return random.choices(product_types, product_fraud)
    elif fraud == False:
        return random.choices(product_types, product_non_fraud)
    else:
        return random.choices(product_types)


def random_currency(fraud=None):
    if fraud == True:
        return random.choices(currencies, currencies_f_purchase)
    elif fraud == False:
        return random.choices(currencies, currencies_nf_purchase)
    else:
        return random.choices(currencies)


## fix the time points and location
def random_time(start=2000, end=2024):
    # Generate random values for year, month, day, hour, minute, second, microsecond
    year = random.randint(start, end)  # Adjust the range as needed
    month = random.randint(1, 12)
    day = random.randint(1, 28)  # Assuming all months have up to 28 days for simplicity
    hour = random.randint(0, 23)
    minute = random.randint(0, 59)
    second = random.randint(0, 59)
    microsecond = random.randint(0, 999999)

    # Create a datetime object with the random values

    # Create a datetime object with the random values
    random_datetime = datetime(year, month, day, hour, minute, second, microsecond)

    return random_datetime.strftime("%Y-%m-%d %H:%M:%S.%f")[:-5]

def custom_key(date_string):
    return datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S.%f")

def sorted_random_times(num, start=2000, end=2024):
    x = [random_time(start, end) for i in range(num)]
    return sorted(x, key=custom_key)


def random_location():
    latitude = random.uniform(-90, 90)
    longitude = random.uniform(-180, 180)
    location = (latitude, longitude)
    return location


km_to_miles = lambda km: km * 0.621371


def haversine_distance(coord1, coord2):
    lat1, lon1 = coord1
    lat2, lon2 = coord2

    # Convert latitude and longitude from degrees to radians
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)

    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    # Earth radius in kilometers (you can change it to miles by using 3958.8 instead of 6371)
    radius = 6371
    distance = radius * c
    distance *= 0.621371
    return distance


def select_and_remove(lst, x):
    if x > len(lst):
        return "Error: x is greater than the length of the list"

    selected = random.sample(lst, x)
    for item in selected:
        lst.remove(item)

    return selected, lst

true_false_random = lambda: random.random() < 0.5
true_false_null_random = lambda: random.choices([True, False, None], weights=[0.4, 0.4, 0.2])[0]



def find_time_difference(dt1, dt2):
    difference = dt2 - dt1
    if difference < timedelta(seconds=0):
        difference = timedelta(seconds=0) - difference
    total_seconds = difference.total_seconds()
    days = int(total_seconds // 86400)
    remaining_seconds = total_seconds % 86400
    hours = int(remaining_seconds // 3600)
    remaining_seconds %= 3600
    minutes = int(remaining_seconds // 60)
    seconds = int(remaining_seconds % 60)
    return [days, hours, minutes, seconds]


round_two_decimals = lambda number, decimals=2: round(number, decimals)

def time_list_to_hours(time_list):
    days, hours, minutes, seconds = time_list
    total_seconds = (days * 24 * 3600) + (hours * 3600) + (minutes * 60) + seconds
    return total_seconds / 3600


def max_dist(center, max_distance_miles):
    # Convert max distance from miles to kilometers
    max_distance_km = max_distance_miles / 0.621371

    # Generate random angle in radians
    random_angle = random.uniform(0, 2 * 3.141592653589793)  # 0 to 2*pi

    # Generate random distance in kilometers within the specified range
    random_distance_km = random.uniform(0, max_distance_km)

    # Calculate the new latitude and longitude
    lat, lon = center
    lat_change = random_distance_km / 6371 * (180 / 3.141592653589793)
    lon_change = random_distance_km / 6371 * (180 / 3.141592653589793) / np.cos(lat * (3.141592653589793 / 180))

    new_lat = lat + lat_change
    new_lon = lon + lon_change

    return new_lat, new_lon


def min_dist(center, min_dis):
    a = random_location()
    while haversine_distance(center, a) < min_dis:
        a = random_location()
    return a

def is_year(date_string, year=2024):
    # Split the date string by '-'
    parts = date_string.split('-')

    # Extract the year part
    year_part = int(parts[0])

    # Check if the year matches the provided year
    if year_part == year:
        return True
    else:
        return False
