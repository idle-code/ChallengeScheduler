from django.contrib.auth.models import User
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


class ChallengeForm(ModelForm):
    class Meta:
        model = Challenge
        fields = ["name", "description", "start", "deadline", "todo"]
