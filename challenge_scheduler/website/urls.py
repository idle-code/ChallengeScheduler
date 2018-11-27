from django.urls import path

from .views import AccountSettingsView
from .views import ChallengeActive
from .views import ChallengeEdit
from .views import ChallengeList
from .views import ChallengeReadOnly
from .views import ChallengeRemove
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
    path("challenge/new/", ChallengeEdit.as_view(), name="challenge-full-edit"),
    path("challenge/<int:challenge_id>/", ChallengeReadOnly.as_view(), name="challenge-read-only"),
    path("challenge/<int:challenge_id>/active", ChallengeActive.as_view(), name="challenge-active"),
    path("challenge/<int:challenge_id>/edit", ChallengeEdit.as_view(), name="challenge-edit"),
    path("challenge/<int:challenge_id>/remove", ChallengeRemove.as_view(), name="challenge-remove"),
]
