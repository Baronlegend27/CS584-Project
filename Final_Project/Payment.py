import Val_gen
construct_point = lambda coords: f"({coords[1]}, {coords[0]})"
def generate_fake_payment(index, timing = None):
    amount = Val_gen.random_amount()
    currency = Val_gen.random_currency()
    if timing == None:
        time = Val_gen.random_time()
    else:
        time = timing
    location = Val_gen.random_location()
    return amount, currency, time, construct_point(location), index
