from django.urls import path
from . import views

urlpatterns = [
    path('', views.upload),
    path('/detail', views.detail),
    path('/complete', views.complete)
]
