from django.urls import path

from . import views

urlpatterns = [
    path('comment/add/<slug:slug>', views.add_comment),
]
