from django.urls import path
from . import views

urlpatterns = [
    path('edit', views.edit_profile),
    path('delete', views.delete),
    path('logout', views.CustomLogoutView.as_view()),
]
