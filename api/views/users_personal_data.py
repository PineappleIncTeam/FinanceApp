from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from api.models import User, City, Country
from api.serializers import UserSerializer, CountrySerializer, CitySerializer


@api_view(["GET", "PATCH"])
@permission_classes([IsAuthenticated])
def user_data(request):
    user = request.user
    if request.method == "GET":
        serializer = UserSerializer(user)
        return Response(serializer.data)
    elif request.method == "PATCH":
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def get_countries(request):
    countries = Country.objects.all()
    serializer = CountrySerializer(countries, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def get_cities(request, country_id):
    cities = City.objects.filter(country_id=country_id)
    serializer = CitySerializer(cities, many=True)
    return Response(serializer.data)
