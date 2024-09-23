class Booking:
    def __init__(self, date, time_list, requestor_id):
        self.date = date
        self.time_list = time_list
        self.requestor_id = requestor_id

    def get_date(self):
        return self.date

    def get_time_list(self):
        return self.time_list

    def get_requestor_id(self):
        return self.requestor_id