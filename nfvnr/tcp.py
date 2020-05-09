from django.conf import settings

def inject_settings(request):
    return {
        'pledge_title': settings.PLEDGE_TITLE,
        'organizers_email': settings.ORGANIZERS_EMAIL
    }
