from rest_framework import viewsets, permissions
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response

from api.models import Profile, User
from api.serializers import ProfileSerializer


class ProfileApiView(ListCreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        profile = Profile.objects.get(user=self.request.user.id)
        return Response({"username": profile.username,
                         "email": profile.email,
                         "country": profile.country})

    def post(self, request):
        username = request.user
        user = User.objects.get(email=username)
        us = {"user": user.id,
              "username": user.username,
              "email": user.email,
              "country": user.country,
              # "avatar": None
              }
        print(us)
        serializer = ProfileSerializer(data=us)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
