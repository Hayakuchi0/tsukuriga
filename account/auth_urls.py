from django.urls import path
from . import views

urlpatterns = [
    path('edit', views.edit_profile),
    path('delete', views.delete),
    path('login', views.CustomLoginView.as_view()),
    path('logout', views.CustomLogoutView.as_view()),
    path('import', views.import_user),
]
