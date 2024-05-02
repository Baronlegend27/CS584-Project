from Val_gen import haversine_distance,find_time_difference, round_two_decimals, time_list_to_hours


class DisTime:
    def __init__(self, list, pair, account_id):
        self.pair = pair
        self.account_id = account_id
        self.list = list
        self.time_diff, self.distance = DisTime.find_difference(list)
        self.distance = round_two_decimals(self.distance)
        self.ratio = round_two_decimals(self.distance/time_list_to_hours(self.time_diff))

    @staticmethod
    def find_difference(data):
        dt1, coord1 = data[0]
        dt2, coord2 = data[1]
        time_diff = find_time_difference(dt1, dt2)
        coord1 = eval(coord1)  # Convert string to tuple
        coord2 = eval(coord2)  # Convert string to tuple
        distance = haversine_distance(coord1, coord2)
        return time_diff, distance

    def get_distance(self):
        return self.distance
    def get_ratio(self):
        return self.ratio

    def __str__(self):
        return f'account_id:{self.account_id} pair:{self.pair}'

