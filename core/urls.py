from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('bot.urls')),
    path('admin/', admin.site.urls),

    path('api/', include([
        path('auth/', include('djoser.urls')),
        path('auth/', include('djoser.urls.jwt')),
        path("v1/", include([
            path('users/', include('accounts.urls')),
            path('chat/', include('chat.api.urls')),
        ])),
    ]))
]
