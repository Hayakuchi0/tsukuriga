from django.contrib import admin
from . import models

admin.site.register(models.Video)
admin.site.register(models.UploadedPureVideo)
admin.site.register(models.VideoProfile)
admin.site.register(models.VideoData)
