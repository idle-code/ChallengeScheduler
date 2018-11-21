from django.contrib.auth.models import User
from django.forms import CharField, EmailField, Form, ModelForm, PasswordInput


class LoginForm(Form):
    username = CharField()
    password = CharField(widget=PasswordInput)


class RegisterForm(ModelForm):
    email = EmailField()
    password = CharField(widget=PasswordInput)

    class Meta:
        model = User
        fields = ["email", "username", "password"]
