from django.urls import path, include
from .auth import views

urlpatterns = [
    path('account/', include('account.auth.urls')),
    path('settings/', include('account.settings.urls')),
    path('u/', include('account.users.urls')),
    # django-social-authのエラーハンドリング
    path('complete/<backend>/', views.social_auth_complete)
]
