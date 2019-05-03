from django.urls import path
from . import views

urlpatterns = [
    path('hotline/<slug:hotline_type>/<slug:target>', views.hotline),
]
