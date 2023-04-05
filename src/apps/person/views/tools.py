from django.contrib import messages
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import Group
from django.shortcuts import HttpResponse, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext as _
from django.views.decorators.http import require_http_methods

from apps.person.forms import ChangeOfAspectForm, TransferPupilForm
from apps.person.models import Historic, Person
from apps.publicwork.models import Seeker
from apps.user.models import User
from rcadmin.common import paginator


@login_required
@permission_required("person.add_person")
def import_from_seekers(request):
    queryset = Seeker.objects.filter(
        center=request.user.person.center, is_active=True, status="INS"
    )
    object_list = paginator(queryset, page=request.GET.get("page") or 1)

    context = {
        "object_list": object_list,
        "title": _("import from seekers"),
    }
    return render(request, "person/tools/import_from_seekers.html", context)


@login_required
@permission_required("person.add_person")
def import_seeker(request, id):
    seeker = Seeker.objects.get(id=id)
    if request.method == "POST":
        # creating a new user
        password = BaseUserManager().make_random_password()
        new_user = User.objects.create_user(
            email=seeker.email, password=password
        )
        # add new_user in "user" group
        user_group = Group.objects.get(name="user")
        new_user.groups.add(user_group)
        # updating the new_user.profile
        new_user.profile.social_name = seeker.name
        new_user.profile.gender = seeker.gender
        new_user.profile.city = seeker.city
        new_user.profile.state = seeker.state
        new_user.profile.country = seeker.country
        new_user.profile.image = seeker.image
        new_user.profile.phone = seeker.phone
        new_user.profile.save()
        # updating the new_user.person
        new_user.person.name = seeker.name
        new_user.person.center = seeker.center
        new_user.person.birth = seeker.birth
        # put old historic from publicwork to person observations
        new_user.person.observations += "\n*** Public Work Historic ***"
        seeker_historic = seeker.historicofseeker_set.all()
        for hist in seeker_historic:
            _hist = (
                f"\n- {hist.date} [{hist.occurrence}] {hist.description or ''}"
            )
            new_user.person.observations += _hist
        new_user.person.save()
        message = f"The Person '{new_user.person.name}' has been created!"
        messages.success(request, message)
        # inactive seeker
        seeker.status = "ITD"
        seeker.is_active = False
        seeker.save()

        return redirect("person_detail", id=new_user.person.pk)

    context = {
        "object": seeker,
        "title": _("confirm to import"),
    }
    return render(request, "person/elements/confirm_to_import.html", context)


#  pupil transfer
@login_required
@permission_required("person.add_historic")
def pupil_transfer(request):
    if request.method == "POST":
        person = Person.objects.get(name=request.session["pupil_name"])
        old_center = person.center
        person.center_id = request.POST["center"]
        person.save()
        new_transfer = dict(
            person=person,
            occurrence="TRF",
            date=request.POST["transfer_date"],
            description=f"{old_center} ➔ {person.center}",
            made_by=request.user,
        )
        if request.POST.get("observations"):
            new_transfer["description"] += " | {}".format(
                request.POST["observations"]
            )
        Historic.objects.create(**new_transfer)
        return HttpResponse(headers={"HX-Redirect": reverse("person_home")})

    if not request.session.get("pupil_name"):
        request.session["pupil_name"] = ""

    context = {
        "form": TransferPupilForm(initial={"transfer_date": timezone.now()}),
        "title": _("pupil transfer"),
    }
    return render(request, "person/tools/pupil_transfer.html", context)


#  change of aspect
@login_required
@permission_required("person.add_historic")
def change_of_aspect(request):
    if request.method == "POST":
        person = Person.objects.get(name=request.session["pupil_name"])
        old_aspect = person.get_aspect_display()
        person.aspect = request.POST["aspect"]
        person.aspect_date = request.POST["aspect_date"]
        person.save()
        new_aspect = dict(
            person=person,
            occurrence=request.POST["aspect"],
            date=request.POST["aspect_date"],
            description=f"{old_aspect} ➔ {person.get_aspect_display()}",
            made_by=request.user,
        )
        if request.POST.get("observations"):
            new_aspect["description"] += " | {}".format(
                request.POST["observations"]
            )
        Historic.objects.create(**new_aspect)
        return HttpResponse(headers={"HX-Redirect": reverse("person_home")})

    if not request.session.get("pupil_name"):
        request.session["pupil_name"] = ""

    context = {
        "form": ChangeOfAspectForm(initial={"aspect_date": timezone.now()}),
        "title": _("pupil transfer"),
    }
    return render(request, "person/tools/change_of_aspect.html", context)


#  handlers
@login_required
@permission_required("person.add_historic")
@require_http_methods(["GET"])
def search_pupil_by_name(request):
    template_name = "person/tools/elements/search_results.html"
    results = (
        Person.objects.filter(
            name__icontains=request.GET.get("term"),
            center=request.user.person.center,
            is_active=True,
        )[:10]
        if request.GET.get("term")
        else None
    )

    context = {"results": results}
    return render(request, template_name, context)


@login_required
@permission_required("person.add_historic")
@require_http_methods(["GET"])
def select_pupil_by_name(request):
    request.session["pupil_name"] = request.GET.get("name")
    request.session.modified = True
    return HttpResponse(request.GET.get("name"))
