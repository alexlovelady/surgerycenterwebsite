from django.contrib import admin
from .models import ActivityLog, Analytics

admin.site.register(ActivityLog)
admin.site.register(Analytics)