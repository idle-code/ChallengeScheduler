from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.http import HttpRequest, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import RedirectView, TemplateView


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

    def post(self, request: HttpRequest, *args, **kwargs):
        del args, kwargs
        username = request.POST["username"]
        password = request.POST["password"]
        user: User = authenticate(username=username, password=password)
        if user is not None and user.is_active:
            login(request, user)
        return self.render_to_response({"user": user})


class LogoutView(RedirectView):
    url = reverse_lazy("home")

    def get(self, request: HttpRequest, *args, **kwargs):
        print(f"Logging out {request.user}")
        logout(request)
        return super().get(request, *args, **kwargs)


class RegisterView(TemplateView):
    template_name = "website/register.html"

    def post(self, request: HttpRequest, *args, **kwargs):
        del args, kwargs

        # TODO: actually validate following variables:
        username = request.POST["username"]
        if not username:
            return self.render_to_response({"error_message": "No username provided"})
        email = request.POST["email"]
        if not email:
            return self.render_to_response({"error_message": "No email provided"})
        password = request.POST["password"]
        if not password:
            return self.render_to_response({"error_message": "No password provided"})

        try:
            new_user = User.objects.create_user(username, email, password)
            login(request, new_user)
            return HttpResponseRedirect(reverse("home"))
        except IntegrityError as err:
            return self.render_to_response({"error_message": str(err)})
