from djoser.views import UserViewSet
from django.contrib.auth import get_user_model
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import action

from .serializers import CreateUserSerializer, UserSerializer

User = get_user_model()


class CreateListUserViewSet(generics.ListCreateAPIView):
    queryset = User.objects.all()
    @action(detail=False)
    def me(self, request):
        user = self.context['request'].user
        queryset = User.objects.filter(username=user)
        serializer = UserSerializer(data=queryset)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_200_OK)

