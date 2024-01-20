from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User, Group

from .models import SavedRepair, Projects

admin.site.register(SavedRepair)
admin.site.register(Projects)
