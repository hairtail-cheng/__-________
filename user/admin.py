from django.contrib import admin

# Register your models here.
from user import models


admin.site.register(models.Up)
admin.site.register(models.Video)
admin.site.register(models.User)
