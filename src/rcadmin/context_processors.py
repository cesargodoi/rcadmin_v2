from django.conf import settings


def export_vars(request):
    data = {}
    data["APP_NAME"] = settings.get("APP_NAME", "rc@dmin")
    return data
