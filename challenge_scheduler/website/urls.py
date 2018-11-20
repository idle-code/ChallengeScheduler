from django.urls import path

from .views import ChallengeNew, DummyView, HomeView, LoginView, LogoutView, RegisterView

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("account/login/", LoginView.as_view(), name="account-login"),
    path("account/logout/", LogoutView.as_view(), name="account-logout"),
    path("account/register/", RegisterView.as_view(), name="account-register"),
    path("account/", DummyView.as_view(), name="account-settings"),
    path("challenges/", DummyView.as_view(), name="challenge-list"),
    path("challenge/new", ChallengeNew.as_view(), name="challenge-new"),
]
