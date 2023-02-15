from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import (
    login_required,
    permission_required,
    user_passes_test,
)
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext as _

from rcadmin.common import (
    belongs_center,
    clear_session,
    SEEKER_STATUS,
    LECTURE_TYPES,
    ASPECTS,
    STATUS,
    get_template_and_pagination,
)

from apps.center.models import Center
from apps.person.models import Person
from apps.base.searchs import (
    search_pw_group,
    search_lecture,
    search_seeker,
    search_person,
)

from ..forms import GroupForm
from ..models import (
    Seeker,
    Lecture,
    Listener,
    PublicworkGroup,
    HistoricOfSeeker,
)


@login_required
@permission_required("publicwork.view_publicworkgroup")
def group_home(request):
    LIMIT, template_name, _from, _to, page = get_template_and_pagination(
        request,
        "publicwork/groups/home.html",
        "publicwork/groups/elements/group_list.html",
    )

    if request.GET.get("init") or request.user.groups.filter(
        name="publicwork_jr"
    ):
        count = request.user.person.publicworkgroup_set.count() or None
        object_list = request.user.person.publicworkgroup_set.all() or {}
        clear_session(request, ["pwg", "search", "frequencies"])
    else:
        object_list, count = search_pw_group(
            request, PublicworkGroup, _from, _to
        )

    # add action links
    for item in object_list:
        item.actives = (
            item.members.filter(is_active=True)
            .exclude(status__in=["ITD", "STD", "RST"])
            .count()
        )
        item.click_link = reverse("group_detail", args=[item.pk])

    context = {
        "LIMIT": LIMIT,
        "page": page,
        "counter": (page - 1) * LIMIT,
        "object_list": object_list,
        "count": count,
        "init": True if request.GET.get("init") else False,
        "goback_link": reverse("group_home"),
        "title": _("public work - groups"),
        "centers": [[str(cnt.pk), str(cnt)] for cnt in Center.objects.all()],
        "user_center": str(request.user.person.center.pk),
        "nav": "gp_home",
    }
    return render(request, template_name, context)


@login_required
@permission_required("publicwork.view_publicworkgroup")
def group_detail(request, pk):
    LIMIT, template_name, _from, _to, page = get_template_and_pagination(
        request,
        "publicwork/groups/detail.html",
        "publicwork/groups/elements/seeker_list.html",
    )

    clear_session(request, ["search", "frequencies"])
    belongs_center(request, pk, PublicworkGroup)
    pw_group = PublicworkGroup.objects.get(pk=pk)

    _object_list = pw_group.members.exclude(
        status__in=("ITD", "RST", "STD")
    ).order_by("name")

    count = len(_object_list)
    object_list = _object_list[_from:_to]

    # add action links
    for item in object_list:
        item.to_detail = (
            reverse("seeker_detail", args=[item.pk]) + f"?pwg={pk}"
        )
        item.del_member = reverse("group_remove_member", args=[pk, item.pk])
        item.local = f"{item.city} ({item.state}-{item.country})"

    context = {
        "LIMIT": LIMIT,
        "page": page,
        "counter": (page - 1) * LIMIT,
        "object_list": object_list,
        "count": count,
        "object": pw_group,
        "active_members": len(object_list),
        "title": _("group detail"),
        "nav": "info",
        "table_title": "Members",
    }
    return render(request, template_name, context)


@login_required
@permission_required("publicwork.add_publicworkgroup")
def group_create(request):
    if request.method == "POST":
        pw_group_form = GroupForm(request.POST)
        if pw_group_form.is_valid():
            pw_group_form.save()

            message = f"The Group '{request.POST['name']}' has been created!"
            messages.success(request, message)

        return redirect("group_home")

    group_form = GroupForm(
        initial={
            "made_by": request.user,
            "center": request.user.person.center,
        }
    )

    template_name = "publicwork/groups/forms/group.html"
    context = {
        "form": group_form,
        "callback": reverse("group_create"),
        "title": _("Create group"),
    }
    return render(request, template_name, context)


@login_required
@permission_required("publicwork.change_publicworkgroup")
def group_update(request, pk):
    belongs_center(request, pk, PublicworkGroup)
    pw_group = PublicworkGroup.objects.get(pk=pk)

    if request.method == "POST":
        pw_group_form = GroupForm(request.POST, instance=pw_group)
        if pw_group_form.is_valid():
            pw_group_form.save()
            message = f"The Group '{request.POST['name']}' has been updated!"
            messages.success(request, message)

        return redirect("group_detail", pk=pk)

    pw_group_form = GroupForm(
        instance=pw_group,
        initial={"made_by": request.user},
    )

    template_name = "publicwork/groups/forms/group.html"
    context = {
        "form": pw_group_form,
        "callback": reverse("group_update", args=[pk]),
        "title": _("Update group"),
        "update": True,
    }
    return render(request, template_name, context)


@login_required
@permission_required("publicwork.delete_publicworkgroup")
def group_delete(request, pk):
    belongs_center(request, pk, PublicworkGroup)
    pw_group = PublicworkGroup.objects.get(pk=pk)

    if request.method == "POST":
        if pw_group.members.count() > 0 or pw_group.mentors.count() > 0:
            pw_group.is_active = False
            pw_group.save()
        else:
            pw_group.delete()
        return redirect("group_home")

    template_name = "publicwork/confirm/delete.html"
    context = {
        "object": pw_group,
        "del_link": reverse("group_delete", args=[pk]),
    }
    return render(request, template_name, context)


@login_required
@permission_required("publicwork.add_publicworkgroup")
def group_reinsert(request, pk):
    belongs_center(request, pk, PublicworkGroup)
    pw_group = PublicworkGroup.objects.get(pk=pk)

    if request.method == "POST":
        pw_group.is_active = True
        pw_group.save()
        return redirect("group_home")

    template_name = "publicwork/confirm/reinsert.html"
    context = {
        "object": pw_group,
        "reinsert_link": reverse("group_reinsert", args=[pk]),
    }
    return render(request, template_name, context)


# seeker frequencies
@login_required
@permission_required("publicwork.view_publicworkgroup")
@user_passes_test(
    lambda u: "presidium" not in [pr.name for pr in u.groups.all()]
)
def group_frequencies(request, pk):
    LIMIT, template_name, _from, _to, page = get_template_and_pagination(
        request,
        "publicwork/groups/detail.html",
        "publicwork/groups/elements/frequency_list.html",
    )

    clear_session(request, ["search", "frequencies"])
    belongs_center(request, pk, PublicworkGroup)

    pw_group = PublicworkGroup.objects.get(pk=pk)
    active_members = pw_group.members.exclude(status__in=("ITD", "RST", "STD"))
    _object_list = get_frequencies([mbr.id for mbr in active_members])

    count = len(_object_list)
    object_list = _object_list[_from:_to]

    context = {
        "LIMIT": LIMIT,
        "page": page,
        "counter": (page - 1) * LIMIT,
        "object_list": object_list,
        "count": count,
        "object": pw_group,
        "title": _("group detail | frequencies"),
        "active_members": len(active_members),
        "nav": "frequencies",
        "now": datetime.now().date(),
    }

    return render(request, template_name, context)


# handlers
def get_frequencies(ids):
    seekers = Seeker.objects.filter(id__in=ids)
    status = dict(SEEKER_STATUS)
    frequencies = []
    for seek in seekers:
        seeker = {
            "id": seek.id,
            "name": seek.name,
            "is_active": seek.is_active,
            "center": seek.center,
            "status": status[str(seek.status)],
            "date": seek.status_date,
            "freq": 0,
        }
        if seek.listener_set.count():
            for freq in seek.listener_set.all():
                seeker["freq"] += 1
        frequencies.append(seeker)

    return frequencies


@login_required
@permission_required("publicwork.add_listener")
def group_add_frequencies(request, pk):
    belongs_center(request, pk, PublicworkGroup)
    pw_group = PublicworkGroup.objects.get(pk=pk)

    if request.GET.get("lect_pk"):
        # get lecture
        lecture = Lecture.objects.get(pk=request.GET["lect_pk"])
        # create and prepare frequencies object in session, if necessary
        if not request.session.get("frequencies"):
            request.session["frequencies"] = {
                "lecture": {},
                "listeners": [],
            }
            active_members = [
                m
                for m in pw_group.members.all()
                if m.status not in ("ITD", "STD", "RST")
            ]
            preparing_the_session(request, active_members, lecture)

    if request.method == "POST":
        listeners = get_listeners_dict(request)
        if listeners:
            for listener in listeners:
                new_freq = dict(
                    lecture=lecture,
                    seeker_id=listener["id"],
                    observations=listener["obs"],
                )
                Listener.objects.create(**new_freq)
        return redirect("group_detail", pk=pk)

    LIMIT, template_name, _from, _to, page = get_template_and_pagination(
        request,
        "publicwork/groups/detail.html",
        "publicwork/groups/elements/lecture_list.html",
    )

    object_list, count = search_lecture(request, Lecture, _from, _to)
    # add action links
    for item in object_list:
        item.add_freqs_link = (
            reverse("group_add_frequencies", args=[pk]) + f"?lect_pk={item.pk}"
        )

    context = {
        "LIMIT": LIMIT,
        "page": page,
        "counter": (page - 1) * LIMIT,
        "object_list": object_list,
        "count": count,
        "object": pw_group,
        "title": _("add frequencies"),
        "nav": "add_frequencies",
        "goback": reverse("group_detail", args=[pk]),
        "type_list": LECTURE_TYPES,
        "pk": pk,
    }
    return render(request, template_name, context)


# add member
@login_required
@permission_required("publicwork.change_publicworkgroup")
def group_add_member(request, pk):
    belongs_center(request, pk, PublicworkGroup)
    pw_group = PublicworkGroup.objects.get(pk=pk)

    if request.GET.get("seek_pk"):
        seeker = Seeker.objects.get(pk=request.GET["seek_pk"])

        if request.method == "POST":
            pw_group.members.add(seeker)
            date = timezone.now().date()
            if seeker.status != "MBR":
                HistoricOfSeeker.objects.create(
                    seeker=seeker,
                    occurrence="MBR",
                    date=date,
                    description=f"Entered in '{pw_group}' group.",
                )

            seeker.status = "MBR"
            seeker.status_date = date
            seeker.save()

            messages.success(request, "The member has been inserted on group!")
            return redirect("group_detail", pk=pk)

        template_name = "publicwork/confirm/insert.html"
        context = {
            "object": "{} ➜ {} ({})".format(
                seeker.name, pw_group.name, pw_group.center
            ),
            "confirm_link": "{}?seek_pk={}".format(
                reverse("group_add_member", args=[pk]),
                request.GET["seek_pk"],
            ),
        }
        return render(request, template_name, context)

    LIMIT, template_name, _from, _to, page = get_template_and_pagination(
        request,
        "publicwork/groups/detail.html",
        "publicwork/groups/elements/seeker_list_to_add.html",
    )

    if request.GET.get("init"):
        object_list, count = None, None
        clear_session(request, ["search"])
    else:
        object_list, count = search_seeker(request, Seeker, _from, _to)
        # add action links
        for item in object_list:
            item.add_in_group = reverse("group_add_member", args=[pk])
            item.local = f"{item.city} ({item.state}-{item.country})"

    if not request.htmx and object_list:
        message = f"{count} records were found in the database"
        messages.success(request, message)

    context = {
        "LIMIT": LIMIT,
        "page": page,
        "counter": (page - 1) * LIMIT,
        "object_list": object_list,
        "count": count,
        "object": pw_group,
        "init": True if request.GET.get("init") else False,
        "goback_link": reverse("group_add_member", args=[pw_group.pk]),
        "status_list": [
            stt
            for stt in SEEKER_STATUS
            if stt[0] not in ("OBS", "ITD", "STD", "RST")
        ],
        "only_actives": True,
        "title": _("group add member"),
        "nav": "add_member",
        "goback": reverse("group_detail", args=[pk]),
        "centers": [[str(cnt.pk), str(cnt)] for cnt in Center.objects.all()],
        "user_center": str(request.user.person.center.pk),
        "pk": pk,
    }
    return render(request, template_name, context)


@login_required
@permission_required("publicwork.change_publicworkgroup")
def group_remove_member(request, group_pk, member_pk):
    pw_group = PublicworkGroup.objects.get(pk=group_pk)
    member = Seeker.objects.get(pk=member_pk)

    if request.method == "POST":
        pw_group.members.remove(member)

        return redirect("group_detail", pk=group_pk)

    template_name = "publicwork/confirm/delete.html"
    context = {
        "object": "{} ⛔️ {} ({})".format(
            member.name, pw_group.name, pw_group.center
        ),
        "del_link": reverse("group_remove_member", args=[group_pk, member_pk]),
    }
    return render(request, template_name, context)


# add mentor
@login_required
@permission_required("publicwork.change_publicworkgroup")
def group_add_mentor(request, pk):
    belongs_center(request, pk, PublicworkGroup)
    pw_group = PublicworkGroup.objects.get(pk=pk)

    if request.GET.get("person_pk"):
        person = Person.objects.get(pk=request.GET["person_pk"])

        if request.method == "POST":
            pw_group.mentors.add(person)
            messages.success(
                request, _("The mentor has been inserted on group!")
            )
            return redirect("group_detail", pk=pk)

        template_name = "publicwork/confirm/insert.html"
        context = {
            "object": "{} ➜ {} ({})".format(
                person.name, pw_group.name, pw_group.center
            ),
            "confirm_link": "{}?person_pk={}".format(
                reverse("group_add_mentor", args=[pk]),
                request.GET["person_pk"],
            ),
        }
        return render(request, template_name, context)

    LIMIT, template_name, _from, _to, page = get_template_and_pagination(
        request,
        "publicwork/groups/detail.html",
        "publicwork/elements/person_list.html",
    )

    if request.GET.get("init"):
        object_list, count = None, None
        clear_session(request, ["search"])
    else:
        object_list, count = search_person(request, Person, _from, _to)
        # add action links
        for item in object_list:
            item.add_link = (
                reverse("group_add_mentor", args=[pk])
                + f"?person_pk={ item.pk }"
            )
            item.local = "{} ({}-{})".format(
                item.user.profile.city,
                item.user.profile.state,
                item.user.profile.country,
            )

    if not request.htmx and object_list:
        message = f"{count} records were found in the database"
        messages.success(request, message)

    context = {
        "LIMIT": LIMIT,
        "page": page,
        "counter": (page - 1) * LIMIT,
        "object_list": object_list,
        "count": count,
        "object": pw_group,
        "init": True if request.GET.get("init") else False,
        "goback_link": reverse("group_add_mentor", args=[pw_group.pk]),
        "aspect_list": ASPECTS,
        "status_list": STATUS,
        "title": _("group add mentor"),
        "nav": "add_mentor",
        "goback": reverse("group_detail", args=[pk]),
        "pk": pk,
        "flag": "group",
    }
    return render(request, template_name, context)


@login_required
@permission_required("publicwork.change_publicworkgroup")
def group_remove_mentor(request, group_pk, mentor_pk):
    pw_group = PublicworkGroup.objects.get(pk=group_pk)
    mentor = Person.objects.get(pk=mentor_pk)

    if request.method == "POST":
        pw_group.mentors.remove(mentor)
        return redirect("group_detail", pk=group_pk)

    template_name = "publicwork/confirm/delete.html"
    context = {
        "object": "{} ⛔️ {} ({})".format(
            mentor.name, pw_group.name, pw_group.center
        ),
        "del_link": reverse("group_remove_mentor", args=[group_pk, mentor_pk]),
        # "member": mentor.name,
        # "group": pw_group,
        # "title": _("confirm to remove"),
    }
    return render(request, template_name, context)


# handlers
def preparing_the_session(request, members, lecture):
    # check which frequencies have already been entered
    inserteds = [
        [str(lect.seeker.pk), lect.observations]
        for lect in lecture.listener_set.all()
    ]
    inserteds_pks = [ins[0] for ins in inserteds]
    # adjust frequencies on session
    frequencies = request.session["frequencies"]
    # add lecture
    frequencies["lecture"] = {
        "id": str(lecture.pk),
        "date": str(datetime.strftime(lecture.date, "%d/%m/%Y")),
        "theme": lecture.theme,
        "type": lecture.type,
        "center": str(lecture.center),
    }
    # add frequencies
    frequencies["listeners"] = []
    for seek in members:
        if str(seek.pk) in inserteds_pks:
            for ins in inserteds:
                if str(seek.pk) == ins[0]:
                    listener = {
                        "seeker": {
                            "id": str(seek.pk),
                            "name": seek.short_name,
                            "center": str(seek.center),
                        },
                        "freq": "on",
                        "observations": ins[1],
                    }
                    break
        else:
            listener = {
                "seeker": {
                    "id": str(seek.pk),
                    "name": seek.short_name,
                    "center": str(seek.center),
                },
                "freq": "",
                "observations": "",
            }
        frequencies["listeners"].append(listener)
    # save session
    request.session.modified = True


def get_listeners_dict(request):
    from_post = [
        obj for obj in request.POST.items() if obj[0] != "csrfmiddlewaretoken"
    ]
    listeners = []
    for i in range(1, len(request.session["frequencies"]["listeners"]) + 1):
        listener = {}
        for _lis in from_post:
            lis = _lis[0].split("-")
            if lis[1] == str(i):
                listener[lis[0]] = _lis[1]
        if "freq" in listener.keys():
            listeners.append(listener)
    return listeners
