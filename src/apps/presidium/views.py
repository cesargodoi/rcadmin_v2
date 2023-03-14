import pandas as pd
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render
from django.urls import reverse
from django.utils.translation import gettext as _

from apps.base.utils import (  # get_installed_per_period_dict,
    get_occurrences_per_period_dict,
    get_period_subtitle,
    get_report_file_title,
)
from apps.person.models import Historic, Person
from rcadmin.common import ASPECTS


def home(request):
    pupils = Person.objects.filter(is_active=True).values("aspect")
    total = 0
    aspect_count = []
    for key, value in dict(ASPECTS).items():
        count = {
            "asp": key,
            "aspect": value,
            "count": len([p for p in pupils if p["aspect"] == key]),
        }
        total += count["count"]
        aspect_count.append(count)

    template_name = "presidium/presidium_home.html"
    context = {"aspect_count": aspect_count, "total": total}
    return render(request, template_name, context)


def aspect_per_centers(request, asp):
    rows = (
        Person.objects.filter(is_active=True, aspect=asp)
        .values("center__name", "aspect")
        .order_by("center__name")
    )

    centers = []
    for center in set([row["center__name"] for row in rows]):
        _center = {
            "center": center,
            "count": len(
                [row for row in rows if row["center__name"] == center]
            ),
        }
        centers.append(_center)

    template_name = "presidium/elements/aspect_per_centers.html"
    context = {
        "aspect": dict(ASPECTS)[rows[0]["aspect"]],
        "centers": centers,
        "total": len(rows),
    }
    return render(request, template_name, context)


# reports
@login_required
@permission_required("person.view_person")
def occurrences_per_period(request):
    if request.GET.get("dt1") and request.GET.get("dt2"):
        # get person dict
        _dict = get_occurrences_per_period_dict(
            request, Historic, presidium=True
        )
        if _dict:
            # select columns to report
            columns = [
                "name",
                "center",
                "local",
                "occurrence",
                "description",
                "date",
            ]
            # generate pandas dataframe
            report_data = pd.DataFrame(_dict, columns=columns)
            #  adjust index
            report_data.index += 1
            # prepare file.xslx
            request.session["data_to_file"] = {
                "name": get_report_file_title(request, "Occurrences"),
                "content": report_data.to_json(orient="records"),
            }

            context = {
                "title": _("occurrences per period"),
                "subtitle": "{} - {}".format(
                    get_period_subtitle(request),
                    str(request.user.person.center),
                ),
                "report_data": report_data.to_html(),
                "goback": reverse("person_home") + "?init=on",
                "search": "base/searchs/modal_period.html",
            }

            return render(request, "base/reports/show_report.html", context)

    context = {
        "title": _("occurrences per period"),
        "goback": reverse("presidium:home"),
        "search": "base/searchs/modal_period.html",
    }

    return render(request, "base/reports/show_report.html", context)
