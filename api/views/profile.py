from django.shortcuts import get_object_or_404
from rest_framework import permissions, status
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.response import Response

from api.models import Profile
from api.serializers import ProfileSerializer


class ProfileApiView(RetrieveUpdateAPIView):

    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    http_method_names = ['get', 'patch', 'head', 'options']

    def get_object(self):
        return get_object_or_404(Profile, user=self.request.user)

    def get(self, request, *args, **kwargs):
        """
        получение профиля пользователя
        """
        profile = self.get_object()
        serializer = self.get_serializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def patch(self, request, *args, **kwargs):
        """
        изменение профиля пользователя
        """
        partial = kwargs.pop('partial', True)
        profile = self.get_object()
        serializer = self.get_serializer(profile, data=request.data, partial=partial)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
