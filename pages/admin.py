from django.contrib import admin
from markdownx.admin import MarkdownxModelAdmin
from markdownx.widgets import AdminMarkdownxWidget
from markdownx.models import MarkdownxField
from .models import Page

AdminMarkdownxWidget.template_name = 'pages/form.html'


class CustomMDXModelAdmin(MarkdownxModelAdmin):
    formfield_overrides = {
        MarkdownxField: {'widget': AdminMarkdownxWidget}
    }


admin.site.register(Page, MarkdownxModelAdmin)
