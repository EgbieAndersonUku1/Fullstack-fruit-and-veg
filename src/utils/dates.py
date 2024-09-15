from datetime import datetime

def calculate_days_between_dates(start_date, end_date):
    if not all(isinstance(date, datetime) for date in [start_date, end_date]):
        raise TypeError("Both start_date and end_date must be datetime objects.")
    
    if end_date > start_date:
        raise ValueError("end_date cannot be greater than start_date.")
    
    return (start_date - end_date).days
