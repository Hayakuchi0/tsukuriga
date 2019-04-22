from django.contrib import admin
from django.utils.html import format_html

from markdownx.admin import MarkdownxModelAdmin
from markdownx.widgets import AdminMarkdownxWidget
from .models import Page

AdminMarkdownxWidget.template_name = 'pages/form.html'


class CustomMDXModelAdmin(MarkdownxModelAdmin):
    list_display = ('title', 'slug', 'featured_order', 'created_at', 'is_published', 'page_url')

    @staticmethod
    def page_url(obj):
        return format_html(f'<a href="/pages/{obj.slug}" target="_blank">記事へのリンク</a>')


admin.site.register(Page, CustomMDXModelAdmin)
