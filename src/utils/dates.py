from datetime import datetime
from django.utils.timezone import make_aware


def calculate_days_between_dates(start_date, end_date):
    """
    Calculate the number of days between two dates, considering only the date part and ignoring the time component.

    Args:
        start_date (datetime): The start date.
        end_date (datetime): The end date.

    Returns:
        int: The number of days between start_date and end_date.

    Raises:
        TypeError: If either start_date or end_date is not a datetime object.
        ValueError: If end_date is greater than start_date.
    """
    if not all(is_date_valid(date) for date in [start_date, end_date]):
        raise TypeError(f"Both start_date and end_date must be datetime objects, not {type(start_date)} and {type(end_date)}")
    
    if end_date > start_date:
        raise ValueError("end_date cannot be greater than start_date.")
     
    # Remove the time component by setting microseconds and seconds to zero
    start_date = start_date.replace(microsecond=0, second=0)
    end_date   = end_date.replace(microsecond=0, second=0)
    
    return (start_date - end_date).days



def current_time():
    return make_aware(datetime.now())


def is_date_valid(date):
    return False if not isinstance(date, datetime) else True
      
        