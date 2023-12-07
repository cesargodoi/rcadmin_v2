from django.urls import path

from .views import activity, event, frequencies

# event
urlpatterns = [
    path("", event.event_home, name="event_home"),
    path("<uuid:pk>/detail", event.event_detail, name="event_detail"),
    path("create/", event.event_create, name="event_create"),
    path("<uuid:pk>/update", event.event_update, name="event_update"),
    path("<uuid:pk>/delete", event.event_delete, name="event_delete"),
]

# activity
urlpatterns += [
    path("activity/", activity.activity_home, name="activity_home"),
    path("activity/create", activity.activity_create, name="activity_create"),
    path(
        "activity/<int:pk>/update",
        activity.activity_update,
        name="activity_update",
    ),
    path(
        "activity/<int:pk>/delete",
        activity.activity_delete,
        name="activity_delete",
    ),
]

# frequencies
urlpatterns += [
    path(
        "<uuid:pk>/add-frequencies",
        frequencies.add_frequencies,
        name="add_frequencies",
    ),
    path(
        "<uuid:pk>/choose-initial/<str:char>",
        frequencies.choose_initial,
        name="choose_initial",
    ),
    path(
        "<uuid:pk>/add-remove-frequency/<uuid:person_pk>",
        frequencies.add_remove_frequency,
        name="add_remove_frequency",
    ),
    path(
        "<uuid:pk>/frequency/<uuid:person_id>/delete",
        frequencies.frequency_delete,
        name="frequency_delete",
    ),
]
