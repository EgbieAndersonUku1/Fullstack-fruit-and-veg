import json
from django.http import JsonResponse
from django.contrib import messages
from django.shortcuts import render, redirect
from .utils.password_validator import PasswordStrengthChecker


# Create your views here.


def register(request):
    
    # To do
    # Add the logic here to register 
    # Add the logic to send email to register account
    messages.success(request, "You have successfully registered")
    return redirect("home")



def validate_password(request):
    if request.method == 'POST':
        try:
            
            # Parse JSON body
            data     = json.loads(request.body.decode('utf-8'))
            password = data.get('password')

          
            if not password:
                return JsonResponse({"IS_VALID": False, "message": "Password is required"}, status=400)

            password_checker = PasswordStrengthChecker(password)
            is_valid        = password_checker.is_strong_password()

            # Return JSON response with status 200
            return JsonResponse({
                "IS_VALID": is_valid,
                "message": "Password strength checked"
            }, status=200)

        except json.JSONDecodeError:
            return JsonResponse({"IS_VALID": False, "message": "Invalid JSON"}, status=400)

   
    return JsonResponse({"IS_VALID": False, "message": "Invalid request method"}, status=405)
    