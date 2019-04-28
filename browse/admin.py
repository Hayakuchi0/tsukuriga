from django.contrib import admin
from . import models


class RankingAdmin(admin.ModelAdmin):
    list_display = ('point', 'video', 'day', 'type')


admin.site.register(models.Ranking, RankingAdmin)
