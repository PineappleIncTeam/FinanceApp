from __future__ import annotations

from typing import TYPE_CHECKING

from django.db import IntegrityError
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.models import User, Profile
from api.serializers.profile import ProfileSerializer

if TYPE_CHECKING:
    from rest_framework.request import Request


class ProfileApiView(ListCreateAPIView):
    # serializer_class = ProfileSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request: Request):
        username = str(self.request.user)
        user = User.objects.get(email=username)

        return Response({"email": user.email, "name": user.username})

    def post(self, request: Request):
        username = str(self.request.user)
        user = User.objects.get(email=username)
        try:
            Profile.objects.create(user=user)
            return Response({"id": f"{user.id}"})
        except IntegrityError:
            user = Profile.objects.get(user=user.id)
            return Response({"id": f"{user}"})
