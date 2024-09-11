from datetime import datetime
from decimal import Decimal


def convert_decimal_to_float(data):
    if isinstance(data, Decimal):
        return float(data)
    elif isinstance(data, dict):
        return {k: convert_decimal_to_float(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [convert_decimal_to_float(i) for i in data]
    return data


def string_to_date(date_str, date_format="%Y-%m-%d"):
    """
    Convert a date string to a date object using the specified format.

    Args:
        date_str (str): The date string to convert.
        date_format (str): The format of the date string (default is '%Y-%m-%d').

    Returns:
        datetime.date: The corresponding date object.
    
    Raises:
        ValueError: If the date_str does not match the date_format.
    """
    return datetime.strptime(date_str, date_format).date()