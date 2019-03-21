from django.urls import path
from . import views

urlpatterns = [
    path('', views.upload),
    path('/import', views.import_upload),
    path('/detail/<slug:slug>', views.detail),
    path('/complete/<slug:slug>', views.complete)
]
