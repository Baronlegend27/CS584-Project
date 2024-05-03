import Val_gen
from Val_gen import true_false_random, min_dist, max_dist
from Val_gen import is_year

construct_point = lambda coords: f"({coords[1]},{coords[0]})"

def basic_purchase_gen(fraud):
    amount = Val_gen.random_amount(larger_values=fraud)
    currency = Val_gen.random_currency(fraud,)
    product_category = Val_gen.random_product(fraud)
    return amount, currency, product_category

class Purchase:
    prior_location = None


    @classmethod
    def init(cls, prior_location):
        cls.prior_location = tuple(prior_location)

    @classmethod
    def purchase(cls, index, time):
        if is_year(time, 2024):
            result = None
        else:
            result = true_false_random()
        if result is None:
            fraud = true_false_random()
        else:
            fraud = result
        amount, currency, product_category = basic_purchase_gen(fraud)
        if fraud:
            location = max_dist(cls.prior_location, 30)
        else:
            location = min_dist(cls.prior_location, 30)

        cls.prior_location = location

        return amount, currency, time, construct_point(location), product_category, index, result
