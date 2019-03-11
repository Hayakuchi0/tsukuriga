from django.urls import path
from . import views

urlpatterns = [
    path('', views.top),
    path('watch/<slug:slug>', views.watch),
    path('edit/<slug:slug>', views.edit),
]
