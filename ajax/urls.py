from django.urls import path

from . import views

urlpatterns = [
    path('comments/add/<slug:slug>', views.add_comment),
    path('comments/delete/<int:pk>', views.delete_comment),
    path('comments/list/<slug:slug>', views.list_comments),
    path('points/add/<slug:slug>', views.add_point),
    path('points/list/<slug:slug>', views.list_points),
    path('favorites/toggle/<slug:slug>', views.toggle_favorite),
    path('favorites/list/<slug:slug>', views.list_favorites),
    path('direct_message/add/<slug:slug>', views.post_direct_message),
    path('direct_message/list/<slug:slug>', views.list_direct_message),
]
