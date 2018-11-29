# from django.contrib import admin
# Register your models here.
from django.contrib import admin

from .models import Challenge
from .models import Milestone
from .models import ProgressEntry

admin.site.register(Challenge)
admin.site.register(Milestone)
admin.site.register(ProgressEntry)
