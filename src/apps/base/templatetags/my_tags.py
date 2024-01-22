from datetime import date
from django import template
from django.contrib.auth.models import Group
from rcadmin.common import short_name

register = template.Library()


@register.filter(name="age")
def age(birth):
    return (date.today() - birth).days // 365


@register.filter(name="shortname")
def shortname(name):
    return short_name(name)


@register.filter(name="has_group")
def has_group(user, group_name):
    group = Group.objects.get(name=group_name)
    return True if group in user.groups.all() else False
