from django.urls import path
from . import views

urlpatterns = [
    path('chat', views.Chat.as_view()),
]
