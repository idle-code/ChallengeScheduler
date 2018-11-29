from datetime import date
from datetime import timedelta
from typing import Dict
from typing import List
from typing import NewType
from typing import Optional

from django.contrib.auth.models import User
from django.db import models
from django.db.models import CharField
from django.db.models import DateField
from django.db.models import DateTimeField
from django.db.models import ForeignKey
from django.db.models import TextField
from django.utils import timezone


Date = NewType("Date", date)


def date_range(start_date, end_date):
    for days in range(int((end_date - start_date).days + 1)):
        yield start_date + timedelta(days)


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

    @property
    def is_active(self) -> bool:
        current_date = timezone.now().date()
        return self.start < current_date <= self.deadline

    @property
    def all_progress_entries(self) -> Dict[Date, Optional["ProgressEntry"]]:
        progress_entries = {}
        created_entries: List[ProgressEntry] = list(self.progress_entries.all())
        edited_entries: Dict[Date, ProgressEntry] = dict(
            map(lambda e: tuple((e.entry_date, e)), created_entries)
        )
        for entry_date in date_range(self.start, self.deadline):
            if entry_date in edited_entries:
                progress_entries[entry_date] = edited_entries[entry_date]
            else:
                progress_entries[entry_date] = None
        return progress_entries

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"Challenge({self})"


class Milestone(models.Model):
    name = CharField(max_length=100)
    deadline = DateField(null=True, blank=True)
    fulfilled_on = DateField(null=True, blank=True)
    challenge = ForeignKey(Challenge, on_delete=models.CASCADE, related_name="milestones")

    @property
    def fulfilled(self) -> bool:
        return self.fulfilled_on is not None

    def __str__(self):
        fulfilled_mark = "[X]" if self.fulfilled else "[ ]"
        if self.deadline:
            return f"{fulfilled_mark} {self.name} ({self.deadline})"
        return f"{fulfilled_mark} {self.name}"


class ProgressEntry(models.Model):
    entry_date = DateField()
    description = TextField()
    challenge = ForeignKey(Challenge, on_delete=models.CASCADE, related_name="progress_entries")

    def __str__(self):
        return f"{self.entry_date}: {self.description}"

    class Meta:
        unique_together = ("entry_date", "challenge")
