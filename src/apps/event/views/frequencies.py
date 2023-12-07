from django.http import HttpResponse
from django.template.loader import render_to_string
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.http import require_http_methods
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.translation import gettext as _

from apps.person.models import Person

from ..forms import FrequenciesAddForm
from ..models import Event, Frequency

from rcadmin.common import get_template_and_pagination, short_name


@require_http_methods(["GET", "DELETE"])
@login_required
@permission_required(["event.change_event", "person.change_person"])
def frequency_delete(request, pk, person_id):
    event = Event.objects.get(pk=pk)
    person = event.frequencies.get(id=person_id)

    if request.method == "DELETE":
        event.frequencies.remove(person)

        LIMIT, template_name, _from, _to, page = get_template_and_pagination(
            request, "event/detail.html", "event/elements/frequency_list.html"
        )

        _object_list = event.frequency_set.all().order_by("person__name_sa")
        count = len(_object_list)
        object_list = _object_list[_from:_to]
        # add action links
        for item in object_list:
            item.del_link = reverse(
                "frequency_delete", args=[pk, item.person.pk]
            )

        context = {
            "LIMIT": LIMIT,
            "page": page,
            "counter": (page - 1) * LIMIT,
            "object_list": object_list,
            "count": count,
        }
        return render(request, template_name, context)

    template_name = "event/confirm/delete.html"
    context = {
        "allowed": True,
        "object": f"{person.name} ⛔️ {event}",
        "del_link": reverse("frequency_delete", args=[pk, person_id]),
    }
    return render(request, template_name, context)


@login_required
@permission_required(["event.change_event", "person.change_person"])
def add_frequencies(request, pk):
    template_name = "event/elements/add_frequencies.html"
    event = Event.objects.get(pk=pk)
    persons = get_persons(event, request.user.person.center, "A")

    context = {
        "object": event,
        "persons": persons,
        "chars": [*"ABCDEFGHIJKLMNOPQRSTUVWXYZ"],
    }
    return render(request, template_name, context)


def choose_initial(request, pk, char):
    template_name = "event/elements/frequencies.html"
    event = Event.objects.get(pk=pk)
    persons = get_persons(event, request.user.person.center, char)

    context = {"persons": persons, "object": event}
    return HttpResponse(
        render_to_string(template_name, context, request),
    )


def add_remove_frequency(request, pk, person_pk):
    template_name = "event/elements/frequency.html"
    event = Event.objects.get(pk=pk)
    _person = Person.objects.get(pk=person_pk)

    frequency, created = Frequency.objects.get_or_create(
        event_id=pk, person_id=person_pk, aspect=_person.aspect
    )

    person = dict(name=short_name(_person.name), pk=_person.pk)

    if created:
        person["in_event"] = True
    else:
        person["in_event"] = False
        frequency.delete()

    context = {"person": person, "object": event}
    return HttpResponse(render_to_string(template_name, context, request))


# handler
def get_persons(event, center, char):
    objects = Person.objects.filter(
        center=center,
        is_active=True,
        name_sa__istartswith=char,
    ).order_by("name_sa")

    persons = []
    for obj in objects:
        person = dict(
            name=short_name(obj.name),
            pk=obj.pk,
            in_event=event in obj.event_set.all(),
        )
        persons.append(person)
    return persons
