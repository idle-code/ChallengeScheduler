from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpRequest
from django.views.generic import RedirectView, TemplateView


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
    url = "/"

    def get(self, request: HttpRequest, *args, **kwargs):
        print("fLogging out {request.user}")
        logout(request)
        return super().get(request, *args, **kwargs)
