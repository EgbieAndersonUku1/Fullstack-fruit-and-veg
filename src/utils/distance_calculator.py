from geopy.distance import geodesic
from datetime import datetime
from django.utils.timezone import is_aware, make_aware
from decimal import Decimal

from utils.validator import validate_required_keys


def is_travel_impossible(last_coordinates:dict, current_coordinates:dict, max_speed_kmh:int):
    """
    Check if travel between two coordinates is physically impossible based on speed.
    
    Args:
        last_coordinates    (dict): Dictionary containing 'latitude', 'longitude', and 'timestamp' of the last session.
        current_coordinates (dict): Dictionary containing 'latitude', 'longitude', and 'timestamp' of the current session.
        max_speed_kmh (int): The maximum speed the object you are travelling can move. It must be in Kilometres
    
    Returns:
        bool: True if the travel is impossible, False otherwise.
        
    Example usage:
    
        >>> from datetime import datetime
        >>> last_coordinates = {
                "latitude": 40.7128,  # New York
                "longitude": -74.0060,
                "timestamp": datetime(2025, 1, 18, 12, 0)   # 12 pm
            }
        >>> current_coordinates = {
                "latitude": 51.5074,  # London
                "longitude": -0.1278,
                "timestamp": datetime(2025, 1, 18, 13, 0)   # arrive same day at 1pm
            }
        >>> AIRPLANE_SPEED_KMH = 900
        >>> is_travel_impossible(last_coordinates, current_coordinates, AIRPLANE_SPEED_KMH)
        True  # Travel is impossible at this speed.
        
    """
    
    if not isinstance(last_coordinates, dict) or not isinstance(current_coordinates, dict):
        raise ValueError("Inputs must be dictionaries.")

    required_keys = ["longitude", "latitude", "timestamp"]
    
    for coordinates in [last_coordinates, current_coordinates]:
        
        validate_required_keys(coordinates, required_keys)
        if not isinstance(coordinates["timestamp"], datetime):
            raise ValueError(f"Timestamp must be a datetime object. Got {type(coordinates['timestamp'])}.")

    # Calculate distance and time difference
    distance_in_kilometers = calculate_distance(
                                lat1=last_coordinates["latitude"],
                                lon1=last_coordinates["longitude"],
                                lat2=current_coordinates["latitude"],
                                lon2=current_coordinates["longitude"],
                                )

    time_difference_in_hours = calculate_time_difference_in_hours(
                                    datetime1=last_coordinates["timestamp"],
                                    datetime2=current_coordinates["timestamp"],
                                    )

    if time_difference_in_hours == 0:
        return True  # Instantaneous travel is impossible

    required_speed = distance_in_kilometers / time_difference_in_hours  # speed = distance/time
    
    if required_speed <= max_speed_kmh:
        return False 
    return True
    
    
def calculate_distance(lat1: Decimal| float,
                       lon1: Decimal|float, 
                       lat2: Decimal|float, lon2: float|Decimal,
                       in_kilometers: bool = True) -> float:
    """
    Calculates the geodesic distance between two sets of coordinates (latitude and longitude).
    
    The distance is returned in kilometers by default, but can be returned in miles if `in_kilometers` 
    is set to False.

    :Args:
        lat1 (float): Latitude of the starting point.
        lon1 (float): Longitude of the starting point.
        lat2 (float): Latitude of the ending point.
        lon2 (float): Longitude of the ending point.

    :Raises:
        ValueError: If any of the latitude or longitude values are not of type int or float,
                    or if they are out of valid range for geographic coordinates.
    
    :Returns:
        float: The distance between the two coordinates in kilometers or miles.
    
    :Example usage:
        # New York City, USA (Latitude: 40.7128, Longitude: -74.0060)
        # Los Angeles,   USA (Latitude: 34.0522, Longitude: -118.2437)
        # kilometers
        >>> calculate_distance(40.7128, -74.0060, 34.0522, -118.2437)
        >>> 3944.4222314899216
        
        # miles
        >>> calculate_distance(40.7128, -74.0060, 34.0522, -118.2437, False)
        >>> 2450.950344668338
        
    """
    for coordinate in [lat1, lon1, lat2, lon2]:
         if not isinstance(coordinate, (int, float, Decimal)):
            raise ValueError(f"The value <{coordinate}> is not an int, float, or Decimal. Type {type(coordinate)}")
    
    if not (-90 <= lat1 <= 90 and -90 <= lat2 <= 90):
        raise ValueError("Latitude values must be between -90 and 90 degrees.")
    
    if not (-180 <= lon1 <= 180 and -180 <= lon2 <= 180):
        raise ValueError("Longitude values must be between -180 and 180 degrees.")
    
    distance = geodesic((lat1, lon1), (lat2, lon2))
    
    return distance.kilometers if in_kilometers else distance.miles


def calculate_time_difference_in_hours(datetime1, datetime2):
    """
    Calculate the time difference between two timestamps in hours.
    
    Args:
        datetime1, datetime2 (datetime): This is the datetime object.
    
    Returns:
        float: Time difference in hours.
        
    Example usage
    
    # Define two datetime objects
    >>> last_session_time = datetime(2025, 1, 18, 12, 0, 0)
    >>> current_time      = datetime(2025, 1, 18, 15, 0, 0)
    
    # Calculate the time difference in hours
    >>> time_difference   = calculate_time_difference_in_hours(current_time, last_session_time)
    >>> print(f"Time difference: {time_difference} hours")

    """
    if not isinstance(datetime1, datetime) or not isinstance(datetime2, datetime):
        raise ValueError("The datetime object is not an instance of the datetime object")
    
    is_datetime1_aware, is_datetime2_aware = is_aware(datetime1), is_aware(datetime2)
    
    if is_datetime1_aware != is_datetime2_aware:
        raise ValueError("Both datetime objects must have the same timezone-awareness")

    HOURS_IN_SECONDS = 3600
    
    if not is_datetime1_aware:
        datetime1 = make_aware(datetime1)
    if not is_datetime2_aware:
        datetime2 = make_aware(datetime2)
    
    delta = abs(datetime1 - datetime2)
    return delta.total_seconds() / HOURS_IN_SECONDS


