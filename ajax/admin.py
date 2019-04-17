from django.contrib import admin

from . import models

admin.site.register(models.Comment)
admin.site.register(models.Point)
admin.site.register(models.Favorite)
admin.site.register(models.DirectMessage)
