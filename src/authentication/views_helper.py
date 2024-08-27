
    
import json
from django.http import JsonResponse


def validate_helper(request, field_name, succ_message, validation_func):
    if request.method == 'POST':
        try:
            # Parse JSON body
            data = json.loads(request.body.decode('utf-8'))
            resp = data.get(field_name)

            if not resp:
                return JsonResponse({"IS_VALID": False, "message": f"{field_name.title()} is required"}, status=400)

            # Use the passed validation function
            is_valid = validation_func(resp)

            print(is_valid)
            # Return JSON response with appropriate message
            return JsonResponse({
                "IS_VALID": is_valid,
                "message": succ_message if is_valid else f"{field_name.title()} is already in use",
            }, status=200)

        except json.JSONDecodeError:
            return JsonResponse({"IS_VALID": False, "message": "Invalid JSON"}, status=400)

    return JsonResponse({"IS_VALID": False, "message": "Invalid request method"}, status=405)
