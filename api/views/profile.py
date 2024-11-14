from rest_framework import permissions
from rest_framework.parsers import FormParser,  MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import Profile, User
from api.serializers import ProfileSerializer


class ProfileApiView(APIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = (FormParser, MultiPartParser)

    def get(self, request):
        """
        Getting user profile data
        """

        profile = Profile.objects.get(user=self.request.user.id)
        return Response({"first_name": profile.first_name,
                         "last_name": profile.last_name,
                         "gender": profile.gender,
                         "country": profile.country.code,
                         # "avatar": profile.avatar,
                         })

    def patch(self, request):
        """
        Save the user to the model profile
        """
        Profile.objects.filter(user = self.request.user.id).update(
            first_name = request.data["first_name"],
            last_name = request.data["last_name"],
            gender = request.data["gender"],
            country = request.data["country"],
            avatar = request.data["avatar"]
        )
        return Response({"post": {"first_name": request.data["first_name"],
                         "last_name": request.data["last_name"],
                         "gender": request.data["gender"],
                         "country": request.data["country"]}})
