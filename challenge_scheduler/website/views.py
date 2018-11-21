from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import RedirectView, TemplateView

from .forms import LoginForm, RegisterForm


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
            if user is not None and user.is_active:
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
            new_user = form.save()
            login(request, new_user)
            return HttpResponseRedirect(reverse("home"))
        return self.render_to_response({"form": form})


class ChallengeNew(TemplateView):
    template_name = "website/challenge-new.html"

    def post(self, request: HttpRequest, *args, **kwargs):
        del request
        del args, kwargs

        return self.render_to_response({})
