# from __future__ import annotations
#
# from typing import TYPE_CHECKING
#
# from django.db import IntegrityError
# from rest_framework.generics import ListCreateAPIView
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.response import Response
#
# from api.models import User, Profile
# from api.serializers.profile import ProfileSerializer
#
# if TYPE_CHECKING:
#     from rest_framework.request import Request
#
#
# class ProfileApiView(ListCreateAPIView):
#     # serializer_class = ProfileSerializer
#     permission_classes = (IsAuthenticated,)
#
#     def get(self, request: Request):
#         username = str(self.request.user)
#         user = User.objects.get(email=username)
#
#         return Response({"email": user.email, "name": user.username})
#
#     def post(self, request: Request):
#         username = str(self.request.user)
#         user = User.objects.get(email=username)
#         try:
#             Profile.objects.create(user=user)
#             return Response({"id": f"{user.id}"})
#         except IntegrityError:
#             user = Profile.objects.get(user=user.id)
#             return Response({"id": f"{user}"})


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

#
# from rest_framework import viewsets, permissions
# from api.models import Profile
# from api.serializers import ProfileSerializer
#
# class ProfileViewSet(viewsets.ModelViewSet):
#     queryset = Profile.objects.all()
#     serializer_class = ProfileSerializer
#     permission_classes = [permissions.IsAuthenticated]
#
#     def get_queryset(self):
#         # Возвращает профиль только текущего пользователя
#
#         user = self.request.user
#         serializer = ProfileSerializer(user, data=self.request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#         return Profile.objects.filter(user=self.request.user)
#
#     def perform_create(self, serializer):
#         # Присваивает текущего пользователя профилю
#         serializer.save(user=self.request.user)
