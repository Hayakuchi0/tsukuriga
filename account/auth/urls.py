from django.urls import path
from . import views

urlpatterns = [
    path('signup', views.signup),
    path('login', views.CustomLoginView.as_view()),
    path('logout', views.CustomLogoutView.as_view()),
    path('import', views.import_user),
]
