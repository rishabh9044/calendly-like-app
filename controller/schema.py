from datetime import datetime, timedelta
from controller.api_instance import api
from flask_restx import fields, ValidationError
import pdb
# def validate_date_list(value):
#     date_list = value.get("date_list")
#     one_month_from_now = (datetime.now() + timedelta(days=30)).date()
#     pdb.set_trace()
#     for date_str in date_list:
#         try:
#             breakpoint()
#             print(date_str)
#             date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
#             print(date_obj)
#             breakpoint()
#         except ValueError:
#             raise ValueError(f"Invalid date format for '{date_str}'. Expected format: YYYY-MM-DD")
#
#         if date_obj > one_month_from_now:
#             raise ValueError(f"Date '{date_str}' is more than one month from now")
#
#     return value

# def validate_time_range(value):
#     start_time, end_time = value["start_time"], value["end_time"]
#
#     # Validate individual time values
#     try:
#         start_datetime = datetime.strptime(start_time, "%H:%M")
#         end_datetime = datetime.strptime(end_time, "%H:%M")
#     except ValueError:
#         raise ValueError("Invalid time format. Use HH:MM format.")
#
#     # Check if time values are within 24 hours
#     if start_datetime.hour > 23 or start_datetime.minute > 59:
#         raise ValueError("Invalid start time. Hour and minute should be within 0-23 and 0-59 respectively.")
#     if end_datetime.hour > 23 or end_datetime.minute > 59:
#         raise ValueError("Invalid end time. Hour and minute should be within 0-23 and 0-59 respectively.")
#
#     if end_datetime < start_datetime:
#         end_datetime += timedelta(days=1)
#
#     time_diff = end_datetime - start_datetime
#     if time_diff.total_seconds() > 24 * 3600:
#         raise ValueError("Time range should not exceed 24 hours")
#
#     return value

def validate_date_format(date_str):
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        raise ValidationError(f"Invalid date format for '{date_str}'. Expected format: YYYY-MM-DD")

def validate_time_format(time_str):
    try:
        datetime.strptime(time_str, "%H:%M")
    except ValueError:
        raise ValidationError(f"Invalid time format for '{time_str}'. Expected format: HH:MM")
#Schema definition for all the Requests/Responses

hello_world_model = api.model('HelloWorld', {
    'message': fields.String(required=True, description='The Hello World message')
})

add_user_model = api.model('AddUser', {
    'user_name': fields.String(required=True, description='Name of user'),
    'phone_number': fields.String(required=True, description='Phone number')
})

add_user_response_model = api.model('AddUserResponse', {
    'message': fields.String(description='Message'),
    'user_id': fields.Integer(description='User id')
})

get_user_model = api.model('GetUser', {
    'user_id': fields.Integer(description='User id')
})

time_range_model = api.model('TimeRange', {
    'start_time': fields.String(description='Start time in HH:MM format', example='09:00'),
    'end_time': fields.String(description='End time in HH:MM format', example='17:00')
})

set_user_availability_model = api.model('SetUserAvailability', {
    'user_id': fields.Integer(description='User id'),
    'date_list': fields.List(fields.String(), description='List of dates'),
    'time_ranges': fields.List(fields.List(fields.Nested(time_range_model), description='List of lists of time ranges'))
})

get_overlap_model = api.model('GetOverlap', {
    'user_id_1': fields.Integer(description='User id'),
    'user_id_2': fields.Integer(description='User id')
})

book_meeting_model = api.model('BookMeeting', {
    'user_id': fields.Integer(required=True, description='User ID'),
    'requestor_id': fields.Integer(description='Requestor ID'),
    'date': fields.String(required=True, description='Date in YYYY-MM-DD format'),
    'start_time': fields.String(required=True, description='Start time in HH:MM format'),
    'end_time': fields.String(required=True, description='End time in HH:MM format')
})
get_bookings_model = api.model('GetBookings', {
    'user_id': fields.Integer(description='User id')
})
