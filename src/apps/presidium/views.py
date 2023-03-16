import pandas as pd
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render
from django.urls import reverse
from django.utils.translation import gettext as _

from apps.base.utils import (
    get_installed_per_period_dict,
    get_occurrences_per_period_dict,
    get_period_subtitle,
    get_report_file_title,
)
from apps.person.models import Historic, Person
from rcadmin.common import ASPECTS


def home(request):
    return render(request, "presidium/presidium_home.html")


def pupils_by_aspect(request):
    rows = Person.objects.filter(is_active=True).values("aspect")
    total = 0
    object_list = []
    for key, value in dict(ASPECTS).items():
        count = {
            "asp": key,
            "aspect": value,
            "count": len([p for p in rows if p["aspect"] == key]),
        }
        total += count["count"]
        object_list.append(count)

    template_name = "presidium/elements/pupils_by_aspect.html"
    context = {"object_list": object_list, "total": total}
    return render(request, template_name, context)


def pupils_by_aspect_per_centers(request, asp):
    rows = (
        Person.objects.filter(is_active=True, aspect=asp)
        .values("center__name", "aspect")
        .order_by("center__name")
    )
    object_list = []
    for center in set([row["center__name"] for row in rows]):
        _center = {
            "center": center,
            "count": len(
                [row for row in rows if row["center__name"] == center]
            ),
        }
        object_list.append(_center)

    template_name = "presidium/elements/pupils_by_aspect_per_centers.html"
    context = {
        "aspect": dict(ASPECTS)[rows[0]["aspect"]],
        "object_list": object_list,
        "total": len(rows),
    }
    return render(request, template_name, context)


def pupils_by_center(request):
    rows = (
        Person.objects.filter(is_active=True)
        .values("center__name", "center_id")
        .order_by("center__name")
    )
    centers = set([(row["center__name"], row["center_id"]) for row in rows])
    object_list = []
    for center, center_id in centers:
        _center = {
            "center": center,
            "center_id": center_id,
            "count": len(
                [row for row in rows if row["center__name"] == center]
            ),
        }
        object_list.append(_center)

    template_name = "presidium/elements/pupils_by_center.html"
    context = {"object_list": object_list, "total": len(rows)}
    return render(request, template_name, context)


def pupils_by_center_per_aspects(request, center_id):
    rows = (
        Person.objects.filter(is_active=True, center_id=center_id)
        .values("center__name", "aspect")
        .order_by("aspect")
    )
    total = 0
    object_list = []
    for key, value in dict(ASPECTS).items():
        count = {
            "aspect": value,
            "count": len([p for p in rows if p["aspect"] == key]),
        }
        total += count["count"]
        object_list.append(count)

    template_name = "presidium/elements/pupils_by_center_per_aspects.html"
    context = {
        "center": rows[0]["center__name"],
        "object_list": object_list,
        "total": len(rows),
    }
    return render(request, template_name, context)


# reports
@login_required
@permission_required("person.view_person")
def installed_per_period(request):
    if request.GET.get("dt1") and request.GET.get("dt2"):
        # get person dict
        _dict = get_installed_per_period_dict(request, Person, presidium=True)
        if _dict:
            # select columns to report
            columns = ["name", "local", "center", "date"]
            # generate pandas dataframe
            report_data = pd.DataFrame(_dict, columns=columns)
            report_data.fillna("", inplace=True)
            #  adjust index
            report_data.index += 1
            # prepare file.xslx
            request.session["data_to_file"] = {
                "name": get_report_file_title(request, "New_Pupils"),
                "content": report_data.to_json(orient="records"),
            }

            context = {
                "title": _("installed per period"),
                "subtitle": get_period_subtitle(request),
                "report_data": report_data.to_html(),
                "goback": reverse("presidium:home"),
                "search": "base/searchs/modal_period.html",
            }
            return render(request, "base/reports/show_report.html", context)

    context = {
        "title": _("installed per period"),
        "goback": reverse("presidium:home"),
        "search": "base/searchs/modal_period.html",
    }
    return render(request, "base/reports/show_report.html", context)


@login_required
@permission_required("person.view_person")
def occurrences_per_period(request):
    if request.GET.get("dt1") and request.GET.get("dt2"):
        _dict = get_occurrences_per_period_dict(
            request, Historic, presidium=True
        )
        if _dict:
            columns = [
                "name",
                "center",
                "local",
                "occurrence",
                "description",
                "date",
            ]
            report_data = pd.DataFrame(_dict, columns=columns)
            report_data["description"] = report_data["description"].str.slice(
                0, 30
            )
            report_data.fillna("", inplace=True)
            report_data.index += 1
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
                "goback": reverse("presidium:home"),
                "search": "base/searchs/modal_period.html",
            }
            return render(request, "base/reports/show_report.html", context)

    context = {
        "title": _("occurrences per period"),
        "goback": reverse("presidium:home"),
        "search": "base/searchs/modal_period.html",
    }
    return render(request, "base/reports/show_report.html", context)
