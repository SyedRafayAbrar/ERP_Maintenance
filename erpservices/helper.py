from django.http import HttpRequest
from rest_framework.request import Request

def adapt_drf_request_to_django(request):
    # Assuming 'request' is an instance of rest_framework.request.Request
    django_request = HttpRequest()
    
    # Copy relevant attributes from DRF request to Django request
    django_request.method = request.method
    django_request.GET = request.GET
    django_request.POST = request.POST
    django_request.FILES = request.FILES
    django_request.path = request.path
    django_request.user = request.user  # If needed

    # Add any other attributes you might need

    return django_request