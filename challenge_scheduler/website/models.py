from django.contrib.auth.models import User
from django.db import models
from django.db.models import CharField
from django.db.models import DateField
from django.db.models import DateTimeField
from django.db.models import ForeignKey
from django.db.models import TextField


class Challenge(models.Model):
    name = CharField(max_length=100)
    symbol = CharField(max_length=6, blank=True)
    description = TextField()
    start = DateField()
    deadline = DateField()
    todo = TextField(blank=True)
    created = DateTimeField(auto_now_add=True)
    last_modified = DateTimeField(auto_now=True)
    owner = ForeignKey(User, on_delete=models.CASCADE)


class Milestone(models.Model):
    name = CharField(max_length=100)
    deadline = DateField(null=True, blank=True)
    fulfilled_on = DateField(null=True, blank=True)
    challenge = ForeignKey(Challenge, on_delete=models.CASCADE)

    @property
    def fulfilled(self) -> bool:
        return self.fulfilled_on is not None


class ProgressEntry(models.Model):
    entry_date = DateField()
    description = TextField()
    challenge = ForeignKey(Challenge, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("entry_date", "challenge")
