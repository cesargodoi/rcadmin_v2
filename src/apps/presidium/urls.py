from django.urls import path

from . import views

app_name = "presidium"

urlpatterns = [
    path("", views.home, name="home"),
    path("pupils-by-aspect/", views.pupils_by_aspect, name="pupils_by_aspect"),
    path("pupils-by-center/", views.pupils_by_center, name="pupils_by_center"),
    path(
        "pupils-by-aspect/per-center/<str:asp>",
        views.pupils_by_aspect_per_centers,
        name="pupils_by_aspect_per_centers",
    ),
    path(
        "pupils-by-center/per-aspects/<str:center_id>",
        views.pupils_by_center_per_aspects,
        name="pupils_by_center_per_aspects",
    ),
    path(
        "reports/installed-per-period/",
        views.installed_per_period,
        name="installed_per_period",
    ),
    path(
        "reports/occurrences-per-center/",
        views.occurrences_per_period,
        name="occurrences_per_period",
    ),
]
