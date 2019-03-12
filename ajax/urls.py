from django.urls import path

from . import views

urlpatterns = [
    path('comments/add/<slug:slug>', views.add_comment),
]
