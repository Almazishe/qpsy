from django.urls import path, include

urlpatterns = [
    path('cities/', include('locations.city.urls')),
    path('regions/', include('locations.region.urls')),
    path('schools/', include('locations.school.urls')),
]
