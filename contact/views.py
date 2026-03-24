import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .models import ContactMessage


@csrf_exempt
@require_POST
def submit_contact(request):
    """Handle contact form submissions via AJAX POST."""
    try:
        data = json.loads(request.body)
        name = data.get('name', '').strip()
        email = data.get('email', '').strip()
        message = data.get('message', '').strip()

        # Basic validation
        if not name or not email or not message:
            return JsonResponse({
                'status': 'error',
                'message': 'All fields are required.'
            }, status=400)

        # Save to database
        ContactMessage.objects.create(
            name=name,
            email=email,
            message=message
        )

        return JsonResponse({
            'status': 'success',
            'message': 'Your message has been sent successfully! I will get back to you soon.'
        })

    except json.JSONDecodeError:
        return JsonResponse({
            'status': 'error',
            'message': 'Invalid data format.'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': 'Something went wrong. Please try again later.'
        }, status=500)
