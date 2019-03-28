from django.urls import path
from . import views

urlpatterns = [
    path('edit', views.edit_profile),
    path('logout', views.CustomLogoutView.as_view()),
]
