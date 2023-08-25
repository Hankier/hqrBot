from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from base.models import Ping

@csrf_exempt
@require_http_methods(["POST"])
def create_or_increment_ping(request):
    """
    This view allows the creation of a new Ping instance with a given dc_user or
    increments the ping_count of an existing instance.
    """
    try:
        dc_user = int(request.POST['dc_user'])
    except (KeyError, ValueError):
        return HttpResponse("Invalid 'dc_user' provided.", status=400)

    # Try to get the Ping instance with the provided dc_user
    # If it doesn't exist, create a new one with ping_count set to 1
    ping_instance, created = Ping.objects.get_or_create(dc_user=dc_user, defaults={'ping_count': 1})

    # If the Ping instance already exists, increment the ping_count
    if not created:
        ping_instance.ping_count += 1
        ping_instance.save()

    return JsonResponse({'dc_user': dc_user, 'ping_count': ping_instance.ping_count})

@require_http_methods(["GET"])
def get_ping_value(request, dc_user):
    """
    This view returns the ping_count value for a specific dc_user.
    """
    try:
        ping_instance = Ping.objects.get(dc_user=dc_user)
        return JsonResponse({'dc_user': dc_user, 'ping_count': ping_instance.ping_count})
    except Ping.DoesNotExist:
        return HttpResponse(f"No record found for dc_user: {dc_user}", status=404)

