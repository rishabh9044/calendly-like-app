class Availability:
    def __init__(self, date, time_list):
        self.date = date
        self.time_list = time_list
    def get_date(self):
        return self.date
    def get_time_list(self):
        return self.time_list