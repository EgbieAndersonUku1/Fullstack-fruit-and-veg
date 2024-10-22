import json
from django.http import JsonResponse

from django.http import JsonResponse
import json


def create_json_response(is_valid, message, status):
    """Helper function to create a JSON response."""
    return JsonResponse({"IS_VALID": is_valid, "message": message}, status=status)


def validate_json_and_respond(request, field_name, follow_up_message, validation_func):
    """
    Validates JSON data in a POST request and returns a JSON response.

    This function handles the validation of JSON-based requests by extracting a specific field from the request 
    body and applying a custom validation function to its value. It uses the following steps:

    Args:
        request (HttpRequest): The incoming Django request object, expected to be a POST request with JSON data.
        field_name (str): The key in the JSON data whose value needs to be validated.
        follow_up_message (str): The message to display if the validation is successful.
        validation_func (callable): A function that takes the extracted field value and returns a tuple:
            - is_valid (bool): Indicates if the validation was successful.
            - error_msg (str or None): The error message to display if validation fails.

    Returns:
        JsonResponse: A Django JsonResponse indicating the success or failure of the request, with an appropriate 
        message and status code:
            - 200 if validation succeeds.
            - 422 if the field is missing or validation fails.
            - 400 for invalid JSON format.
            - 405 for non-POST request methods.

     Example usage:
        def validate_email(value):
            if '@' in value:
                return True, ""
            return False, "Invalid email format"

        response = validate_json_and_respond(request, "email", "Email validated successfully", validate_email)
     """
    if request.method != 'POST':
        return create_json_response(False, "Invalid request method", 405)

    try:
        data = json.loads(request.body.decode('utf-8'))
        resp = data.get(field_name)

        if not resp:
            return create_json_response(False, f"{field_name.title()} is required", 422)

        is_valid, error_msg = validation_func(resp)
        message             = follow_up_message if is_valid else (error_msg or 'Invalid input. Please review and try again.')

        return create_json_response(is_valid, message, 200 if is_valid else 422)

    except json.JSONDecodeError:
        return create_json_response(False, "Invalid JSON", 400)
