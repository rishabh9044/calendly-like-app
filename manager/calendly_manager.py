from utils.exceptions import UserNotFoundException, DateOutOfBoundException, SlotNotAvailableException
from models.user_model import User
from models.booking_model import Booking
from utils.helper_functions import init_availability, merge_time_ranges, find_overlapping_ranges


class UserManager:
    def __init__(self):
        self.users = {}

    def add_user(self, user_name, phone) -> int:
        """
        Add new user
        :param user_name: user name
        :param phone:  Phone
        :return: user_id
        """
        user_id = len(self.users) + 1
        user = User(user_id, user_name, phone)
        user.set_availability(init_availability())
        self.users[user.get_user_id()] = user
        return user_id

    def get_user(self, user_id) -> User:
        """
        Get user from user id
        :param user_id: User id
        :return: User class object from user list
        """
        if user_id in self.users:
            return self.users[user_id]
        else:
            raise UserNotFoundException(f"User {user_id} not found")

    def update_availability(self, user_id, date_list, time_slots_list) -> dict:
        """
        Update availability of user
        :param user_id: User id of user
        :param date_list: List of dates to update availability for
        :param time_slots_list: List of list of slots for all the above dates
        :return: dict if updated successfully
        """
        if user_id not in self.users:
            raise UserNotFoundException(f"User {user_id} not found")
        user = self.users[user_id]
        for date, time_range in zip(date_list, time_slots_list):
            availability_dict = user.get_availability()
            if date in availability_dict:
                existing_ranges = availability_dict.get(date).get_time_list()
                new_ranges = existing_ranges + time_range
                merged_ranges = merge_time_ranges(new_ranges)
                user.availability[date].time_list = merged_ranges
            else:
                raise DateOutOfBoundException(f"date {date} is more than one month from now")
        return {'message': 'Availability updated successfully'}

    def get_availability(self, user_id) -> dict:
        """
        Get Availability based on user id
        :param user_id: User id
        :return: dict of availability for a user
        """
        if user_id not in self.users:
            raise UserNotFoundException(f"User {user_id} not found")
        user = self.users[user_id]
        availability = {}
        for date, avail_obj in user.get_availability().items():
            availability[date] = avail_obj.get_time_list()
        return availability

    def get_overlapping_availability(self, user_id1, user_id2) -> dict:
        """
        Get Overlapping intervals between 2 users
        :param user_id1: user id of first user
        :param user_id2: user id of second user
        :return: dict of overlapping availability
        """
        if user_id1 in self.users and user_id2 in self.users:
            user1 = self.users[user_id1]
            user2 = self.users[user_id2]
            overlapping_availability = {}
            for date in set(user1.get_availability().keys()) & set(user2.get_availability().keys()):
                ranges1 = user1.get_availability().get(date).get_time_list()
                ranges2 = user2.get_availability().get(date).get_time_list()
                overlapping_ranges = find_overlapping_ranges(ranges1, ranges2)
                if overlapping_ranges:
                    overlapping_availability[date] = overlapping_ranges
            return overlapping_availability
        else:
            raise UserNotFoundException(f"Either User {user_id1} or User {user_id2} not found")

    def book_meeting(self, user_id, date, start_time, end_time, requestor_id):
        """
        Book a meeting for a user on a specific date and time range
        :param requestor_id: id of requestor
        :param user_id: User ID
        :param date: Date in YYYY-MM-DD format
        :param start_time: Start time in HH:MM format
        :param end_time: End time in HH:MM format
        :return: Booking status message
        """
        if user_id not in self.users:
            raise UserNotFoundException(f"User {user_id} not found")

        user = self.users[user_id]
        availability_dict = user.get_availability()

        if date not in availability_dict:
            raise DateOutOfBoundException(f"Date {date} is more than one month from now")

        time_range = {'start_time': start_time, 'end_time': end_time}
        existing_ranges = availability_dict[date].get_time_list()
        updated_ranges = []

        for existing_range in existing_ranges:
            if existing_range['start_time'] <= start_time and existing_range['end_time'] >= end_time:
                # The requested time range is within an available time slot
                for existing_range in existing_ranges:
                    # Check if the existing range overlaps with the booked range
                    if existing_range['start_time'] >= end_time or existing_range['end_time'] <= start_time:
                        updated_ranges.append(existing_range)
                    else:
                        if existing_range['start_time'] < start_time:
                            updated_ranges.append({'start_time': existing_range['start_time'], 'end_time': start_time})

                        if existing_range['end_time'] > end_time:
                            updated_ranges.append({'start_time': end_time, 'end_time': existing_range['end_time']})

                # The requested time range is available, proceed with booking
                user.availability[date].time_list = updated_ranges
                booked_meetings = user.get_booked_meetings()
                if date not in booked_meetings:
                    booked_meetings[date] = []
                booking = Booking(date, [time_range], requestor_id)
                booked_meetings[date].append(booking)
                user.book_meeting(booked_meetings)
                return {'message': 'Booking successful'}
        else:
            # The requested time range is not within any available time slot
            raise SlotNotAvailableException(f"The requested time slot {start_time} to {end_time} is not available")

    def get_meetings(self, user_id):
        """
        Get the booked meetings for a user
        :param user_id: User ID
        :return: Dictionary of booked meetings
        """
        if user_id not in self.users:
            raise UserNotFoundException(f"User {user_id} not found")

        user = self.users[user_id]
        booked_meetings = {}
        for date, bookings in user.get_booked_meetings().items():
            booked_meetings[date] = [
                {
                    'time_list': booking.get_time_list(),
                    'requestor_id': booking.get_requestor_id(),
                    'requestor_name': self.users[booking.get_requestor_id()].get_name(),
                    'requestor_phone': self.users[booking.get_requestor_id()].get_phone()

                }
                for booking in bookings
            ]
        return booked_meetings