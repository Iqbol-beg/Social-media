from django.contrib import admin
from . import models

admin.site.register(models.User)
admin.site.register(models.Post)
admin.site.register(models.Followers)
admin.site.register(models.Comment)
admin.site.register(models.Like)