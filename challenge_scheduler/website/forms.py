from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import CharField
from django.forms import DateField
from django.forms import EmailField
from django.forms import Form
from django.forms import ModelForm
from django.forms import modelformset_factory
from django.forms import PasswordInput
from django.forms import TextInput

from .models import Challenge
from .models import Milestone


class BootstrapForm(Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field_widget_class = field.widget.attrs.get("class", "")
            field.widget.attrs.update({"class": field_widget_class + " form-control"})


class LoginForm(BootstrapForm):
    username = CharField()
    password = CharField(widget=PasswordInput)


class RegisterForm(ModelForm, BootstrapForm):
    email = EmailField()
    password = CharField(widget=PasswordInput)

    class Meta:
        model = User
        fields = ["email", "username", "password"]


class AccountSettingsForm(ModelForm, BootstrapForm):
    email = EmailField()
    password = CharField(widget=PasswordInput)
    password_retype = CharField(widget=PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        if password:
            password_retype = cleaned_data.get("password_retype")
            if password != password_retype:
                raise ValidationError("Entered passwords differ")
        return cleaned_data

    class Meta:
        model = User
        fields = ["email", "password", "password_retype"]


class MilestoneEditForm(ModelForm, BootstrapForm):
    deadline = DateField(
        widget=TextInput(attrs={"data-provide": "datepicker", "class": "datainput"}), required=False
    )

    class Meta:
        model = Milestone
        fields = ["name", "deadline"]


MilestoneEditFormset = modelformset_factory(Milestone, MilestoneEditForm, extra=1, can_delete=True)


class ChallengeEditForm(ModelForm, BootstrapForm):
    # TODO: user datepicker in data range mode
    start = DateField(widget=TextInput(attrs={"data-provide": "datepicker", "class": "datainput"}))
    deadline = DateField(
        widget=TextInput(attrs={"data-provide": "datepicker", "class": "datainput"})
    )

    # milestones = None

    class Meta:
        model = Challenge
        fields = ["name", "symbol", "description", "start", "deadline"]


class ChallengeActiveForm(ModelForm, BootstrapForm):
    progress_entries = None

    class Meta:
        model = Challenge
        fields = ["todo"]
