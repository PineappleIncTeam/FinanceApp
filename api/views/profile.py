from django.forms import model_to_dict
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
        """
        Getting user profile data
        """

        profile = Profile.objects.get(user=self.request.user.id)
        return Response({"first_name": profile.first_name,
                         "last_name": profile.last_name,
                         "gender": profile.gender,
                         "country": profile.country,
                         # "avatar": profile.avatar,
                         })

    def post(self, request):
        """
        Save the user to the model profile
        """
        post_new = Profile.objects.filter(user = self.request.user.id).update(
            first_name = request.data["first_name"],
            last_name = request.data["last_name"],
            gender = request.data["gender"],
            country = request.data["country"]
        )
        return Response({"post": post_new})
