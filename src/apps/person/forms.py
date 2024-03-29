from django import forms
from django.utils.translation import gettext_lazy as _

from apps.user.models import Profile, User
from rcadmin.common import (
    HIDDEN_AUTH_FIELDS,
    OCCURRENCES,
    OCCURRENCES_AND_STATUS,
)

from .models import Historic, Invitation, Person


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["email"]


class ProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields["city"].required = True
        self.fields["state"].required = True

    class Meta:
        model = Profile
        fields = ["gender", "city", "state", "country"]


class PersonForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PersonForm, self).__init__(*args, **kwargs)
        self.fields["birth"].required = True

    class Meta:
        model = Person
        fields = ["name", "birth", "is_active", "made_by", "observations"]
        widgets = {
            "observations": forms.Textarea(attrs={"rows": 2}),
            "birth": forms.widgets.DateInput(
                format="%Y-%m-%d", attrs={"type": "date"}
            ),
        }
        widgets.update(HIDDEN_AUTH_FIELDS)


class HistoricForm(forms.ModelForm):
    occurrence = forms.ChoiceField(choices=OCCURRENCES_AND_STATUS)

    class Meta:
        model = Historic
        fields = "__all__"
        widgets = {
            "description": forms.Textarea(attrs={"rows": 2}),
            "date": forms.widgets.DateInput(
                format="%Y-%m-%d", attrs={"type": "date"}
            ),
            "person": forms.HiddenInput(),
            "made_by": forms.HiddenInput(),
        }


class HistoricUpdateForm(HistoricForm):
    occurrence = forms.ChoiceField(choices=OCCURRENCES)


# partial forms
class ProfileFormUpdate(forms.ModelForm):
    class Meta:
        model = Profile
        fields = "__all__"
        exclude = ["user", "image"]


class PupilFormUpdate(forms.ModelForm):
    class Meta:
        model = Person
        fields = "__all__"
        exclude = [
            "user",
            "center",
            "status",
            "aspect",
            "aspect_date",
            "is_active",
            "made_by",
        ]
        widgets = {
            "observations": forms.Textarea(attrs={"rows": 3}),
            "birth": forms.widgets.DateInput(
                format="%Y-%m-%d", attrs={"type": "date"}
            ),
        }


class ImageFormUpdate(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["image"]


# invite person
class InvitationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(InvitationForm, self).__init__(*args, **kwargs)
        self.fields["birth"].required = True
        self.fields["id_card"].required = True

    class Meta:
        model = Invitation
        fields = ["name", "email", "birth", "id_card", "center"]
        widgets = {
            "birth": forms.widgets.DateInput(
                format="%Y-%m-%d", attrs={"type": "date"}
            ),
            "email": forms.widgets.EmailInput(),
            "center": forms.HiddenInput(),
        }


#  pupil registration form  ###################################################
help_text = {
    "email": (
        "Você não pode alterar o seu email neste momento, pois ele foi \
        pré-cadastrado no sistema e é necessário para a validação deste \
        formuário.  Você poderá fazer a troca depois através da secretaria."
    ),
    "sos_contact": (
        "Indique uma pessoa de sua confiança, para que possamos entrar em \
        contato em um eventual caso de emergência envolvendo você."
    ),
}

popover = {
    "data-trigger": "hover",
    "data-container": "body",
    "data-toggle": "popover",
    "data-placement": "right",
}


class PupilRegistrationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PupilRegistrationForm, self).__init__(*args, **kwargs)
        self.fields["birth"].required = True
        self.fields["gender"].required = True
        self.fields["id_card"].required = True
        self.fields["address"].required = True
        self.fields["number"].required = True
        self.fields["complement"].required = False
        self.fields["district"].required = True
        self.fields["city"].required = True
        self.fields["state"].required = True
        self.fields["zip_code"].required = True
        self.fields["phone"].required = True

    class Meta:
        model = Invitation
        fields = "__all__"
        exclude = ["imported"]
        widgets = {
            "birth": forms.widgets.DateInput(
                format="%Y-%m-%d", attrs={"type": "date"}
            ),
            "email": forms.widgets.EmailInput(
                attrs={
                    "readonly": "readonly",
                    "title": "Importante!",
                    "data-content": help_text["email"],
                    **popover,
                }
            ),
            "sos_contact": forms.widgets.TextInput(
                attrs={
                    "title": "Porque Contato de Emergência?",
                    "data-content": help_text["sos_contact"],
                    **popover,
                }
            ),
            "sos_phone": forms.widgets.TextInput(
                attrs={
                    "title": "Porque Contato de Emergência?",
                    "data-content": help_text["sos_contact"],
                    **popover,
                }
            ),
            "center": forms.HiddenInput(),
            "invited_on": forms.HiddenInput(),
        }


class TransferPupilForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(TransferPupilForm, self).__init__(*args, **kwargs)
        self.fields["center"].required = True
        self.fields["center"].label = _("Transfer to Center")
        self.fields["observations"].label = _("Some observations")
        self.fields["transfer_date"].label = _("Transfer date")

    transfer_date = forms.DateField(
        widget=forms.widgets.DateInput(
            format="%Y-%m-%d", attrs={"type": "date"}
        ),
    )

    class Meta:
        model = Person
        fields = ["center", "observations"]

        widgets = {"observations": forms.Textarea(attrs={"rows": 1})}


class ChangeOfAspectForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ChangeOfAspectForm, self).__init__(*args, **kwargs)
        self.fields["aspect"].required = True
        self.fields["aspect"].label = _("Select new Aspect")
        self.fields["observations"].label = _("Some observations")

    class Meta:
        model = Person
        fields = ["aspect", "aspect_date", "observations"]

        widgets = {
            "observations": forms.Textarea(attrs={"rows": 1}),
            "aspect_date": forms.widgets.DateInput(
                format="%Y-%m-%d", attrs={"type": "date"}
            ),
        }
