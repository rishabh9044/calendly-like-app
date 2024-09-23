import json
from textwrap import indent

from flask import Flask, request, Response
from flask_restx import Api, Resource, fields

from controller.schema import hello_world_model, add_user_model, add_user_response_model, get_user_model, \
    time_range_model, set_user_availability_model, get_overlap_model, book_meeting_model, get_bookings_model
from utils.exceptions import UserNotFoundException, DateOutOfBoundException, SlotNotAvailableException
from manager.calendly_manager import UserManager
from controller.api_instance import api
from utils.helper_functions import validate_time_range, validate_date_list


app = Flask(__name__)
app.config.SWAGGER_UI_URL = '/swagger'
api.init_app(app)


api.models = {
    'HelloWorld': hello_world_model,
    'AddUser': add_user_model,
    'AddUserResponse': add_user_response_model,
    'GetUser': get_user_model,
    'TimeRange': time_range_model,
    'SetUserAvailability': set_user_availability_model,
    'GetOverlap': get_overlap_model,
    'BookMeeting': book_meeting_model,
    'GetBookings': get_bookings_model,
}

user_ns = api.namespace('Users', description='User related operations')
meeting_ns = api.namespace('Meetings', description='Meeting related operations')
availability_ns = api.namespace('Availability', description='Availability related operations')

#In memory DB
user_manager = UserManager()


@api.route('/hello')
class HelloWorld(Resource):
    @api.marshal_with(hello_world_model)
    def get(self):
        """
        Returns a friendly 'Hello World!' message
        """
        return {'message': 'Hello World!'}


@user_ns.route('/add_user')
class AddUser(Resource):
    @api.doc(description="Add new user")
    @api.expect(add_user_model)
    @api.marshal_with(add_user_response_model)
    def post(self):
        """
        Add new user in in-memory db
        """
        name = request.json['user_name']
        phone_number = request.json['phone_number']
        user_id = user_manager.add_user(name, phone_number)
        return {'message': 'User added successfully', 'user_id': user_id}


@user_ns.route('/get_user_availability')
class GetUser(Resource):
    @api.doc(description="Get Availability for a user")
    @api.expect(get_user_model)
    def post(self):
        """
        Get Availability for a user
        """
        user_id = request.json.get("user_id")
        try:
            user = user_manager.get_user(user_id)
            availability = user_manager.get_availability(user_id)
            bookings = user_manager.get_meetings(user_id)
            return Response(json.dumps({
                'user_id': user.get_user_id(),
                'user_name': user.get_name(),
                'phone_number': user.get_phone(),
                'availability': availability,
                'bookings': bookings
            }, indent=4), status=200)
        except UserNotFoundException as e:
            return Response(json.dumps({"error": str(e)}), status=400)


@availability_ns.route('/set_user_availability')
class SetAvailability(Resource):
    @api.doc(description="Set Availability for a user")
    @api.expect(set_user_availability_model, validate=True)
    def post(self):
        """
        Set Availability for a user
        """
        user_id = request.json.get("user_id")
        date_list = request.json.get("date_list")
        time_ranges = request.json.get("time_ranges")
        try:
            validate_time_range(time_ranges)
            validate_date_list(date_list)
            message = user_manager.update_availability(user_id, date_list, time_ranges)
            return Response(json.dumps({"message": message.get("message")}), status=200)
        except ValueError as e:
            return Response(json.dumps({"error": str(e)}), status=422)
        except UserNotFoundException as e:
            return Response(json.dumps({"error": str(e)}), status=400)
        except DateOutOfBoundException as e:
            return Response(json.dumps({"error": str(e)}), status=400)


@availability_ns.route('/get_availability_overlap')
class GetOverlap(Resource):
    @api.doc(description="Get overlap in availability of two users")
    @api.expect(get_overlap_model)
    def post(self):
        """
        Get overlap in availability between two users
        """
        user_id_1 = request.json.get("user_id_1")
        user_id_2 = request.json.get("user_id_2")
        try:
            message = user_manager.get_overlapping_availability(user_id_1, user_id_2)
            return Response(json.dumps({"output": message}, indent=4), status=200)
        except UserNotFoundException as e:
            return Response(json.dumps({"error": str(e)}), status=400)


@meeting_ns.route('/book_meeting')
class BookMeeting(Resource):
    @api.doc(description="Book meeting for a user by a requestor")
    @api.expect(book_meeting_model)
    def post(self):
        """
        Book meeting for a user by a requestor
        """
        user_id = request.json.get("user_id")
        date = request.json.get("date")
        start_time = request.json.get("start_time")
        end_time = request.json.get("end_time")
        requestor_id = request.json.get("requestor_id")
        try:
            validate_time_range([[{'start_time': start_time, 'end_time': end_time}]])
            booking_status = user_manager.book_meeting(user_id, date, start_time, end_time, requestor_id)
            return Response(json.dumps(booking_status, indent=4), 200)
        except ValueError as e:
            return Response(json.dumps({"error": str(e)}), status=422)
        except UserNotFoundException as e:
            return Response(json.dumps({'error': str(e)}), 400)
        except DateOutOfBoundException as e:
            return Response(json.dumps({'error': str(e)}), 400)
        except SlotNotAvailableException as e:
            return Response(json.dumps({'error': str(e)}), 400)

@meeting_ns.route('/get_bookings')
class GetOverlap(Resource):
    @api.doc(description='Get bookings for a user')
    @api.expect(get_bookings_model)
    def post(self):
        """
        Get bookings for a user
        """
        user_id = request.json.get("user_id")
        try:
            output = user_manager.get_meetings(user_id)
            return Response(json.dumps({"booked_meetings": output}, indent=4), status=200)
        except UserNotFoundException as e:
            return Response(json.dumps({"error": str(e)}), status=400)

if __name__ == '__main__':
    app.run(debug=True)
