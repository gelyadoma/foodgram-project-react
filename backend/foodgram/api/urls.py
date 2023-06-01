from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CustomUserViewSet, GetTagViewSet, GetIngredientViewSet, RecipesViewSet

app_name = 'api'

router = DefaultRouter()
router.register('tags', GetTagViewSet, basename='tags')
router.register('ingredients', GetIngredientViewSet, basename='ingredients')
router.register('recipes', RecipesViewSet, basename='recipes')
router.register('users', CustomUserViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
