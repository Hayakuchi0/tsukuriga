from django.urls import path

from . import views

urlpatterns = [
    path('comments/add/<slug:slug>', views.add_comment),
    path('comments/delete/<int:pk>', views.delete_comment),
    path('comments/list/<slug:slug>', views.list_comments),
    path('points/add/<slug:slug>', views.add_point),
    path('points/list/<slug:slug>', views.list_points),
]
