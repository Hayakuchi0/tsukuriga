from django.contrib import admin
from . import models


class ReadOnlyMixin:
    def has_change_permission(self, request, obj=None):
        return False


class VideoProfileInline(ReadOnlyMixin, admin.StackedInline):
    model = models.VideoProfile


class VideoDataInline(ReadOnlyMixin, admin.StackedInline):
    model = models.VideoData


class VideoAdmin(ReadOnlyMixin, admin.ModelAdmin):
    list_display_custom = [
        ('動画ID', 'slug'),
        ('タイトル', 'profile__title')
    ]
    inlines = (VideoProfileInline, VideoDataInline)

    def get_list_display(self, request):

        def display_func(attr_path, field_title):
            attrs = attr_path.split('__')
            r = self.get_queryset(request)[0]
            for attr in attrs:
                r = getattr(r, attr)

            f = lambda x: r
            f.short_description = field_title
            return f, attrs[-1]

        list_display = []
        for field_title, field in self.list_display_custom:
            func, title = display_func(field, field_title)
            setattr(self, title, func)
            list_display.append(title)

        return list_display


admin.site.register(models.Video, VideoAdmin)
admin.site.register(models.UploadedPureVideo)
admin.site.register(models.VideoProfile)
admin.site.register(models.VideoData)
