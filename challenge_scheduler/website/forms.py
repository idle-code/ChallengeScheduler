from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import CharField
from django.forms import EmailField
from django.forms import Form
from django.forms import ModelForm
from django.forms import PasswordInput

from .models import Challenge


class LoginForm(Form):
    username = CharField()
    password = CharField(widget=PasswordInput)


class RegisterForm(ModelForm):
    email = EmailField()
    password = CharField(widget=PasswordInput)

    class Meta:
        model = User
        fields = ["email", "username", "password"]


class AccountSettingsForm(ModelForm):
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


class ChallengeForm(ModelForm):
    class Meta:
        model = Challenge
        fields = ["name", "description", "start", "deadline", "todo"]
