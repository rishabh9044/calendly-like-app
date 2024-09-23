class User:
    def __init__(self, user_id, name, phone):
        self.user_id = user_id
        self.name = name
        self.phone = phone
        self.availability = {}
        self.bookings = {}
    def get_availability(self):
        return self.availability
    def set_availability(self, availability):
        self.availability = availability
    def get_user_id(self):
        return self.user_id
    def get_name(self):
        return self.name
    def get_phone(self):
        return self.phone
    def get_booked_meetings(self):
        return self.bookings
    def book_meeting(self, bookings):
        self.bookings = bookings