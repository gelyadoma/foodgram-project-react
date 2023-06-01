from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CreateListUserViewSet

# basename = 'api'
# router = DefaultRouter()
# router.register('users', CreateListUserViewSet)

urlpatterns = [
    # path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
