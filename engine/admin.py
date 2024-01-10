from django.contrib import admin
from . import models


# Register your models here.

admin.site.register(models.Driver)
admin.site.register(models.DriverChoice)
admin.site.register(models.Race)
admin.site.register(models.TopThreeTip)
admin.site.register(models.ResultRace)

@admin.register(models.UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'score']