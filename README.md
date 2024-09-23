# The Challenge

Build us a REST API for calendly. Remember to support

- Setting own availability
- Showing own availability
- Finding overlap in schedule between 2 users

It is up to you what else to support.

## Expectations

We care about

- Have you thought through what a good MVP looks like? Does your API support that?
- What trade-offs are you making in your design?
- Working code - we should be able to pull and hit the code locally. Bonus points if deployed somewhere.
- Any good engineer will make hacks when necessary - what are your hacks and why?

# The Solution

Developed a calendly like app for P0 assignment. It has the following features/api's

- _add_user_ -> It lets you add new user to the in-memory db 
- _get_user_availability_ -> Users can see their availability based on dates
- _set_user_availability_ -> Users can set their availability for multiple dates and times
- _get_availability_overlap_ -> To view availability overlap between 2 users
- _book_meeting_ -> Requestor can book meeting for a user 
- _get_bookings_ -> See meeting bookings for a user

## Assumptions
1. The Person can only book slots till one month from current date
2. Get availability also shows only one month data.
3. User id is allotted internally using sequencing.
4. The data is stored in memory and on every reload it is lost
5. Validations are done for dates, times and any other Schema/input validations required for the app.
6. User name and phone are not validated.
7. You can set availability in any of 24 hour time window and not based on your timezone.

## Hacks 
1. Used in memory db to avoid db connection issues and supportability
2. The schema validations are not done at schema level but on data processing layer.
3. Used only one month time window to simplify implementation logic.
4. Used light weight flask app and not used production level wsgi like gunicorn.

## Hosting Details
This app is currently hosted on https://rish90444.pythonanywhere.com/

You can find below API details and their sample request/response schema

## API Endpoints

The application provides the following API endpoints:

### User Endpoints

`POST /users/add_user`: Add a new user

Sample Input payload:
```
{
  "user_name": "Foo",
  "phone_number": "1234567890"
}
```
Sample Response
```
{
  "message": "User added successfully",
  "user_id": 1
}
```
###
`POST /users/get_user_availability`: Get user details about availability and bookings

Sample Input payload:
```
{
  "user_id": 1
}
```
Sample Response
```
{
    "user_id": 1,
    "user_name": "string",
    "phone_number": "string",
    "availability": {
        "2024-10-09": [
            {
                "start_time": "10:00",
                "end_time": "16:30"
            }
        ],
        "2024-10-10": [],
    },
    "bookings": {
        "2024-10-09": [
            {
                "time_list": [
                    {
                        "start_time": "09:00",
                        "end_time": "10:00"
                    }
                ],
                "requestor_id": 2,
                "requestor_name": "alice",
                "requestor_phone": "1234"
            },
            {
                "time_list": [
                    {
                        "start_time": "16:30",
                        "end_time": "17:00"
                    }
                ],
                "requestor_id": 3,
                "requestor_name": "Bob",
                "requestor_phone": "222222"
            }
        ]
    }
}
```
### Availability Endpoints
`POST /availability/set_user_availability` : Let's you set the availability

Sample Input Payload

```
{
  "user_id": 1,
  "date_list": [
    "2024-10-09", "2024-10-10"
  ],
  "time_ranges": [
    [
      {
        "start_time": "09:00",
        "end_time": "11:00"
      },
      {
        "start_time": "13:00",
        "end_time": "16:00"
      }
    ],
    [
      {
        "start_time": "10:00",
        "end_time": "11:00"
      },
      {
        "start_time": "15:30",
        "end_time": "16:00"
      }
    ] 
  ]
}
```
Sample Response
```
{"message": "Availability updated successfully"}
```
###
`POST /availability/get_availability_overlap` : To find overlap between availability of two users

Sample Input Payload

```
{
  "user_id_1": 1,
  "user_id_2": 2
}
```

Sample Response
```
{
    "output": {
        "2024-10-09": [
            {
                "start_time": "09:00",
                "end_time": "10:00"
            }
        ]
    }
```

### Meeting Endpoints
`POST /meetings/book_meeting` : Book meeting with the user

Sample Input Payload
```
{
  "user_id": 1,
  "requestor_id": 2,
  "date": "2024-10-09",
  "start_time": "16:30",
  "end_time": "17:00"
}
```
Sample Response

```
{
    "message": "Booking successful"
}
```
###
`POST /meetings/get_bookings` : Get all the bookings for the user

Sample Input Payload
```
{
  "user_id": 1
}
```

Sample Response
```
{
    "booked_meetings": {
        "2024-10-09": [
            {
                "time_list": [
                    {
                        "start_time": "09:00",
                        "end_time": "10:00"
                    }
                ],
                "requestor_id": 2,
                "requestor_name": "string",
                "requestor_phone": "string"
            },
            {
                "time_list": [
                    {
                        "start_time": "16:30",
                        "end_time": "17:00"
                    }
                ],
                "requestor_id": 2,
                "requestor_name": "string",
                "requestor_phone": "string"
            }
        ]
    }
}
```
## How to run locally

### Requirements
Install this using pip3 of your local python version (recommended python 3.9)
- flask
- flask-restx
- Python 3.9

`pip3 install flask, flask-restx`


Before running update directory path in `run.py` file


1. Add project root dir in `line 4` `project_home = '~/PycharmProjects/calendly-like-app/'`
2. Run `python3 run.py` in terminal