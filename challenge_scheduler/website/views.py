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
from django.utils import timezone
from django.views.generic import RedirectView
from django.views.generic import TemplateView

from .forms import AccountSettingsForm
from .forms import ChallengeActiveForm
from .forms import ChallengeEditForm
from .forms import LoginForm
from .forms import MilestoneActiveFormSet
from .forms import MilestoneEditFormSet
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


class ChallengeEdit(TemplateView):
    template_name = "website/challenge-full-edit.html"

    def get(self, request: HttpRequest, *args, challenge_id=None, **kwargs):
        del args, kwargs
        if challenge_id:
            challenge = Challenge.objects.get(pk=challenge_id)
            challenge_form = ChallengeEditForm(instance=challenge)
            milestones_formset = MilestoneEditFormSet(
                queryset=challenge.milestones.all(), prefix="milestone"
            )
        else:
            challenge_form = ChallengeEditForm()
            milestones_formset = MilestoneEditFormSet()
        return self.render_to_response(
            {"challenge_form": challenge_form, "milestones_formset": milestones_formset}
        )

    def post(self, request: HttpRequest, *args, challenge_id=None, **kwargs):
        del args, kwargs

        if challenge_id:
            challenge = Challenge.objects.get(pk=challenge_id)
            challenge_form = ChallengeEditForm(request.POST, instance=challenge)
            milestones_formset = MilestoneEditFormSet(
                request.POST, queryset=challenge.milestones.all(), prefix="milestone"
            )
        else:
            challenge_form = ChallengeEditForm(request.POST)
            milestones_formset = MilestoneEditFormSet(request.POST)

        if not challenge_form.is_valid() or not milestones_formset.is_valid():
            return self.render_to_response(
                {"challenge_form": challenge_form, "milestones_formset": milestones_formset}
            )

        new_challenge = challenge_form.save(commit=False)
        if not new_challenge.symbol:
            # Use first name character as symbol
            new_challenge.symbol = new_challenge.name.strip()[0].upper()
        new_challenge.owner = request.user
        new_challenge.save()

        for deleted_milestone_form in milestones_formset.deleted_forms:
            print(f"Deleting {deleted_milestone_form.instance}")
            deleted_milestone_form.instance.delete()
            milestones_formset.forms.remove(deleted_milestone_form)

        for milestone_form in milestones_formset.forms:
            if not milestone_form.cleaned_data.get("name"):
                print(f"Skipping empty form: {milestone_form}")
                continue
            milestone = milestone_form.save(commit=False)
            milestone.challenge = new_challenge
            milestone.save()
            print(f"New milestone created: {milestone}")

        challenge_form = ChallengeEditForm(instance=new_challenge)
        milestones_formset = MilestoneEditFormSet(
            queryset=new_challenge.milestones.all(), prefix="milestone"
        )
        return self.render_to_response(
            {"challenge_form": challenge_form, "milestones_formset": milestones_formset}
        )


class ChallengeReadOnly(TemplateView):
    template_name = "website/challenge-read-only.html"

    def get(self, request: HttpRequest, challenge_id: int, *args, **kwargs):
        del args, kwargs
        challenge = Challenge.objects.get(pk=challenge_id)
        return self.render_to_response({"challenge": challenge})


class ChallengeActive(TemplateView):
    template_name = "website/challenge-active.html"

    def get(self, request: HttpRequest, *args, challenge_id=None, **kwargs):
        del args, kwargs
        if challenge_id:
            challenge = Challenge.objects.get(pk=challenge_id)
            challenge_form = ChallengeActiveForm(instance=challenge)
            milestones_formset = MilestoneActiveFormSet(
                queryset=challenge.milestones.all(), prefix="milestone"
            )
        else:
            challenge_form = ChallengeActiveForm()
            milestones_formset = MilestoneActiveFormSet()
        return self.render_to_response(
            {"challenge_form": challenge_form, "milestones_formset": milestones_formset}
        )

    def post(self, request: HttpRequest, *args, challenge_id=None, **kwargs):
        del args, kwargs

        if challenge_id:
            challenge = Challenge.objects.get(pk=challenge_id)
            challenge_form = ChallengeActiveForm(request.POST, instance=challenge)
            milestones_formset = MilestoneActiveFormSet(
                request.POST, queryset=challenge.milestones.all(), prefix="milestone"
            )
        else:
            challenge_form = ChallengeActiveForm(request.POST)
            milestones_formset = MilestoneActiveFormSet(request.POST)

        if not challenge_form.is_valid() or not milestones_formset.is_valid():
            return self.render_to_response(
                {"challenge_form": challenge_form, "milestones_formset": milestones_formset}
            )

        new_challenge = challenge_form.save(commit=False)
        if not new_challenge.symbol:
            # Use first name character as symbol
            new_challenge.symbol = new_challenge.name.strip()[0].upper()
        new_challenge.owner = request.user
        new_challenge.save()

        for milestone_form in milestones_formset.forms:
            if not milestone_form.cleaned_data.get("fulfilled"):
                print(f"Skipping empty form: {milestone_form}")
                continue
            milestone = milestone_form.save(commit=False)
            milestone.challenge = new_challenge
            milestone.fulfilled_on = timezone.now().date()
            print(f"Milestone marked as complete on: {milestone.fulfilled_on}")
            milestone.save()

        return self.render_to_response(
            {"challenge_form": challenge_form, "milestones_formset": milestones_formset}
        )


class ChallengeList(TemplateView):
    template_name = "website/challenge-list.html"

    def get(self, request: HttpRequest, *args, **kwargs):
        del args, kwargs
        challenges = Challenge.objects.all()
        return self.render_to_response({"challenges": challenges})


class ChallengeRemove(RedirectView):
    url = reverse_lazy("challenge-list")

    def get(self, request: HttpRequest, challenge_id: int, *args, **kwargs):
        challenge = Challenge.objects.get(pk=challenge_id)
        challenge.delete()
        return super().get(request, *args, **kwargs)
