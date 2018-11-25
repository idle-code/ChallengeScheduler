from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpRequest
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.urls import reverse_lazy
from django.views.generic import RedirectView
from django.views.generic import TemplateView

from .forms import AccountSettingsForm
from .forms import ChallengeForm
from .forms import LoginForm
from .forms import RegisterForm
from .models import Challenge


class DummyView(TemplateView):
    template_name = "website/home.html"


class HomeView(TemplateView, LoginRequiredMixin):
    template_name = "website/home.html"
    login_url = "/login/"

    def get_context_data(self, **kwargs):
        from datetime import datetime

        return {"my_date": datetime.now()}


class LoginView(TemplateView):
    template_name = "website/login.html"

    def get(self, request: HttpRequest, *args, **kwargs):
        del args, kwargs
        empty_form = LoginForm()
        return self.render_to_response({"form": empty_form})

    def post(self, request: HttpRequest, *args, **kwargs):
        del args, kwargs

        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user: User = authenticate(username=username, password=password)
            if user is None:
                form.add_error("username", "Invalid user name or password")
            elif not user.is_active:
                form.add_error("username", "Your user account is inactive")
            else:
                login(request, user)
        return self.render_to_response({"form": form})


class LogoutView(RedirectView):
    url = reverse_lazy("home")

    def get(self, request: HttpRequest, *args, **kwargs):
        print(f"Logging out {request.user}")
        logout(request)
        return super().get(request, *args, **kwargs)


class RegisterView(TemplateView):
    template_name = "website/register.html"

    def get(self, request: HttpRequest, *args, **kwargs):
        del args, kwargs
        empty_form = RegisterForm()
        return self.render_to_response({"form": empty_form})

    def post(self, request: HttpRequest, *args, **kwargs):
        del args, kwargs
        form = RegisterForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(new_user.password)
            form.save()
            login(request, new_user)
            return HttpResponseRedirect(reverse("home"))
        return self.render_to_response({"form": form})


class AccountSettingsView(TemplateView):
    template_name = "website/account-settings.html"

    def get(self, request: HttpRequest, *args, **kwargs):
        del args, kwargs
        logged_user = request.user
        form = AccountSettingsForm(instance=logged_user)
        return self.render_to_response({"form": form})

    def post(self, request: HttpRequest, *args, **kwargs):
        del args, kwargs
        logged_user = request.user
        form = AccountSettingsForm(request.POST, instance=logged_user)
        if form.is_valid():
            user = form.save(commit=False)
            if form.cleaned_data["password"]:
                user.set_password(form.cleaned_data["password"])
                update_session_auth_hash(request, user)
            form.save()
        return self.render_to_response({"form": form})


class ChallengeNew(TemplateView):
    template_name = "website/challenge-new.html"

    def get(self, request: HttpRequest, *args, **kwargs):
        del args, kwargs
        empty_form = ChallengeForm()
        return self.render_to_response({"form": empty_form})

    def post(self, request: HttpRequest, *args, **kwargs):
        del args, kwargs
        form = ChallengeForm(request.POST)
        if form.is_valid():
            new_challenge = form.save(commit=False)
            if not new_challenge.symbol:
                # Use first name character as symbol
                new_challenge.symbol = new_challenge.name.strip()[0].upper()
            new_challenge.owner = request.user
            new_challenge.save()
        return self.render_to_response({"form": form})


class ChallengeList(TemplateView):
    template_name = "website/challenge-list.html"

    def get(self, request: HttpRequest, *args, **kwargs):
        del args, kwargs
        challenges = Challenge.objects.all()
        return self.render_to_response({"challenges": challenges})
