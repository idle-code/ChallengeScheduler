from django.urls import path

from .views import AccountSettingsView
from .views import ChallengeList
from .views import ChallengeNew
from .views import HomeView
from .views import LoginView
from .views import LogoutView
from .views import RegisterView

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("account/login/", LoginView.as_view(), name="account-login"),
    path("account/logout/", LogoutView.as_view(), name="account-logout"),
    path("account/register/", RegisterView.as_view(), name="account-register"),
    path("account/", AccountSettingsView.as_view(), name="account-settings"),
    path("challenges/", ChallengeList.as_view(), name="challenge-list"),
    path("challenge/new", ChallengeNew.as_view(), name="challenge-new"),
]
