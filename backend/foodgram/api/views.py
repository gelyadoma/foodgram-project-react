from djoser.views import UserViewSet
from django.contrib.auth import get_user_model
from rest_framework import generics, status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action

from .serializers import TagSerializer, CreateUserSerializer, UserSerializer
from .models import Tag

User = get_user_model()


class GetTagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

    