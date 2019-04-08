from django.urls import path, include

urlpatterns = [
    path('account/', include('account.auth.urls')),
    path('settings/', include('account.settings.urls')),
    path('u/', include('account.users.urls')),
]
