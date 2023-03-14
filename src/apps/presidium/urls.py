from django.urls import path

from . import views

app_name = "presidium"

urlpatterns = [
    path("", views.home, name="home"),
    path(
        "aspect-per-center/<str:asp>",
        views.aspect_per_centers,
        name="aspect_per_centers",
    ),
    path(
        "occurrences-per-center/",
        views.occurrences_per_period,
        name="occurrences_per_period",
    ),
]
