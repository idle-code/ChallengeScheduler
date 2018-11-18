from django.urls import path

from .views import DummyView, HomeView, LoginView, LogoutView

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("account/login/", LoginView.as_view(), name="account-login"),
    path("account/logout/", LogoutView.as_view(), name="account-logout"),
    path("account/register/", DummyView.as_view(), name="account-register"),
    path("account/", DummyView.as_view(), name="account-settings"),
    path("challenges/", DummyView.as_view(), name="challenge-list"),
    path("challenge/new", DummyView.as_view(), name="challenge-new"),
]
