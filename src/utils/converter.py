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


def string_to_date(date_str: str, date_format: str = "%Y-%m-%d") -> datetime.date:
    """
    Convert a date string to a date object using either ISO 8601 format or a specified format.

    Args:
        date_str (str): The date string to convert. If it contains 'T', it's treated as ISO 8601.
        date_format (str): The format of the date string (default is '%Y-%m-%d').

    Returns:
        datetime.date: The corresponding date object.
    
    Raises:
        ValueError: If the date_str does not match the expected format or ISO format.
    """
    try:
        # Handle ISO 8601 format (e.g., "2023-09-13T22:34:36")
        if "T" in date_str:
            return datetime.fromisoformat(date_str).date()
        
        # Handle custom date formats
        return datetime.strptime(date_str, date_format).date()
    except ValueError:
        raise ValueError(f"Unable to parse date string: {date_str}")