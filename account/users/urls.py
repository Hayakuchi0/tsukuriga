from django.urls import path
from . import views

urlpatterns = [
    path('<str:username>', views.profile),
    path('<str:username>/favorites', views.favorites_list),
    path('<str:username>/direct_messages', views.direct_messages_list),
]
