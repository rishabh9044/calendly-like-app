from datetime import datetime, timedelta
from models.availability_model import Availability


def init_availability() -> dict:
    """
    initialize availability when a user is created
    :return: dict with date as key and value as availability object
    """
    today = datetime.today()
    dates = {}
    for i in range(31):
        date = today + timedelta(days=i)
        date_str = date.strftime('%Y-%m-%d')
        dates[date_str] = Availability(date_str, [])
    return dates


def merge_time_ranges(time_ranges) -> list:
    """
    Simple merge interval logic to merge two time intervals
    :param time_ranges: list of time range
    :return: merged time range
    """
    merged_ranges = []
    time_ranges.sort(key=lambda r: r['start_time'])
    start_time, end_time = time_ranges[0]['start_time'], time_ranges[0]['end_time']
    for time_range in time_ranges[1:]:
        new_start_time, new_end_time = time_range['start_time'], time_range['end_time']
        if end_time < new_start_time:
            merged_ranges.append({'start_time': start_time, 'end_time': end_time})
            start_time, end_time = new_start_time, new_end_time
        else:
            end_time = max(end_time, new_end_time)
    merged_ranges.append({'start_time': start_time, 'end_time': end_time})
    return merged_ranges


def find_overlapping_ranges(ranges1, ranges2) -> list:
    """
    Find overlapping time ranges
    :param ranges1: list of time ranges 1
    :param ranges2: list of time ranges 2
    :return: list of overlapping time ranges
    """
    overlapping_ranges = []
    for r1 in ranges1:
        for r2 in ranges2:
            start_time = max(r1['start_time'], r2['start_time'])
            end_time = min(r1['end_time'], r2['end_time'])
            if start_time < end_time:
                overlapping_ranges.append({'start_time': start_time, 'end_time': end_time})
    return overlapping_ranges

def validate_time_range(time_ranges):
    for time_range in time_ranges:
        for value in time_range:
            start_time, end_time = value["start_time"], value["end_time"]

            # Validate individual time values
            try:
                start_datetime = datetime.strptime(start_time, "%H:%M")
                end_datetime = datetime.strptime(end_time, "%H:%M")
            except ValueError:
                raise ValueError("Invalid time format. Use HH:MM format.")

            # Check if time values are within 24 hours
            if start_datetime.hour > 23 or start_datetime.minute > 59:
                raise ValueError("Invalid start time. Hour and minute should be within 0-23 and 0-59 respectively.")
            if end_datetime.hour > 23 or end_datetime.minute > 59:
                raise ValueError("Invalid end time. Hour and minute should be within 0-23 and 0-59 respectively.")

            if end_datetime < start_datetime:
                end_datetime += timedelta(days=1)

            time_diff = end_datetime - start_datetime
            if time_diff.total_seconds() > 24 * 3600:
                raise ValueError("Time range should not exceed 24 hours")
def validate_date_list(date_list):
    one_month_from_now = (datetime.now() + timedelta(days=30)).date()
    for date_str in date_list:
        try:
            date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            raise ValueError(f"Invalid date format for '{date_str}'. Expected format: YYYY-MM-DD")

        if date_obj > one_month_from_now:
            raise ValueError(f"Date '{date_str}' is more than one month from now")