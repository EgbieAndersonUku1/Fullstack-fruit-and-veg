import json
from django.conf import settings
from django.http import JsonResponse
from django.contrib import messages

from utils.generator import generate_token, generate_verification_url


def validate_helper(request, field_name, follow_up_message, validation_func):
    if request.method == 'POST':
        try:
            # Parse JSON body
            data = json.loads(request.body.decode('utf-8'))
            resp = data.get(field_name)

            if not resp:
                return JsonResponse({"IS_VALID": False, "message": f"{field_name.title()} is required"}, status=400)

            is_valid, error_msg = validation_func(resp)
            
            return JsonResponse({
                "IS_VALID": is_valid,
                "message": follow_up_message if is_valid else (error_msg or 'There was a problem with your request. Please review and submit again.'),
            }, status=200)

        except json.JSONDecodeError:
            return JsonResponse({"IS_VALID": False, "message": "Invalid JSON"}, status=400)

    return JsonResponse({"IS_VALID": False, "message": "Invalid request method"}, status=405)



def send_verification_email(request, user, subject, follow_up_message, send_func):
    """
    Sends a verification email using the provided sending function.

    This function generates a new verification code for the user, constructs the verification URL, 
    and sends an email using the specified sending function. It also handles success and error messages 
    based on the email sending response.

    Parameters:
    
    - request (HttpRequest): The HTTP request object.
    - user (User): The user object for whom the email is being sent.
    - subject (str): The subject line of the email.
    - follow_up_message (str): A message to display upon successful email sending.
    - send_func (function): A function responsible for sending the email. This function should accept
      the following parameters:
        - `subject` (str): The subject line of the email.
        - `from_email` (str): The sender's email address.
        - `user` (User): The user object, which typically contains `user.email` and `user.username`.
        - `verification_url` (str): The URL that the user should visit to complete the verification process.
      Example functions could include:
        - `send_verification_email(subject, from_email, user, verification_url)`: Sends a registration verification email.
        - `send_forgotten_password_email(subject, from_email, user, verification_url)`: Sends a password reset email.
        - `send_account_activation_email(subject, from_email, user, verification_url)`: Sends an account activation email.

    Returns:
    - bool: True if the email was sent successfully, False otherwise.
    """

    
    user.set_verification_code(code=generate_token(), expiry_minutes=4320)  # Expires in 3 days
    verification_url = generate_verification_url(request, user)
    
    try:
        # Call the specified send function
        resp = send_func(
            subject=subject,
            from_email=settings.EMAIL_HOST_USER,
            user=user,
            verification_url=verification_url
        )

        if resp:
            messages.success(request, follow_up_message)
        else:
            messages.error(request, "Failed to send email")
            
        return resp

    except Exception as e:
        messages.error(request, "An unexpected error occurred while sending the email. Please try again later.")
        
        return False


