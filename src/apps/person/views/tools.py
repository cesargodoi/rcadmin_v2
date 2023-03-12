from django.contrib import messages
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import Group
from django.shortcuts import HttpResponse, redirect, render
from django.utils.translation import gettext as _
from django.views.decorators.http import require_http_methods

from apps.person.forms import TransferPupilForm
from apps.person.models import Person
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
def pupil_transfer(request):
    if not request.session.get("transfer"):
        request.session["transfer"] = {"person": {}}

    form = TransferPupilForm()

    context = {
        "form": form,
        "title": _("pupil transfer"),
    }
    return render(request, "person/tools/pupil_transfer.html", context)


@require_http_methods(["GET"])
def search_pupil_to_transfer(request):
    template_name = "person/tools/elements/search_results.html"
    results = (
        Person.objects.filter(
            name__icontains=request.GET.get("term"),
            center=request.user.person.center,
        )[:10]
        if request.GET.get("term")
        else None
    )

    context = {"results": results}
    return render(request, template_name, context)


@require_http_methods(["GET"])
def select_pupil_to_transfer(request):
    _name = request.GET.get("name")
    _id = request.GET.get("id")
    request.session["transfer"]["person"] = {"name": _name, "id": _id}
    request.session.modified = True
    print(request.session["transfer"])
    return HttpResponse(_name)
