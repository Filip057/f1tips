from django.contrib import admin
from . import models


# Register your models here.

admin.site.register(models.Driver)
admin.site.register(models.Race)
admin.site.register(models.TopThreeTip)
admin.site.register(models.ResultRace)
admin.site.register(models.AuthUser)
admin.site.register(models.UserProfile)


