from io import BytesIO

import pandas as pd
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.http.response import Http404
from django.shortcuts import render

from apps.center.models import Center


@login_required
def home(request):
    if request.user.person.center:
        center = Center.objects.get(id=request.user.person.center.id)
    elif Center.objects.count() > 0:
        center = Center.objects.first()
    else:
        raise Http404

    context = {"object": center}
    return render(request, "base/home.html", context)


def change_color_scheme(request):
    if (
        not request.session.get("color_theme")
        or request.session["color_theme"] == "light"
    ):
        request.session["color_theme"] = "dark"
    else:
        request.session["color_theme"] = "light"

    return HttpResponse(headers={"HX-Refresh": "true"})


def error_404(request, exception):
    return render(request, "base/404.html", status=404)


def error_500(request):
    return render(request, "base/500.html", status=500)


def clear_session(request):
    for key in request.session.keys():
        del request.session[key]


def get_file(request):
    file = request.session["data_to_file"]
    df = pd.read_json(file["content"])

    if "since" in df.columns:
        df["since"] = df["since"].div(60 * 60 * 24 * 1000)
    if "date" in df.columns:
        df["date"] = df["date"].dt.strftime("%Y-%m-%d")

    buffer = BytesIO()

    with pd.ExcelWriter(buffer) as writer:
        df.to_excel(writer, index=False)

    buffer.seek(0)

    mime = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    response = HttpResponse(buffer, content_type=mime)
    response["Content-Disposition"] = f"attachment; filename={file['name']}"
    return response
