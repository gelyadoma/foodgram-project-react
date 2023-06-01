from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import GetTagViewSet

basename = 'api'
router = DefaultRouter()
router.register('tags', GetTagViewSet)
# router.register('users', CreateListUserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
