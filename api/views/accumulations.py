from __future__ import annotations

from typing import TYPE_CHECKING

from rest_framework.generics import (CreateAPIView, ListAPIView,
                                     ListCreateAPIView,
                                     RetrieveUpdateDestroyAPIView)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import (HTTP_200_OK, HTTP_202_ACCEPTED,
                                   HTTP_404_NOT_FOUND)
from rest_framework.views import APIView

from api.business_logic import (archive_accumulation_target,
                                get_accumulation_info, get_accumulations,
                                get_categories,
                                get_total_amount_of_accumulations)
from api.business_logic.errors import (InvalidNumberOfItemsError,
                                       TargetDoesNotExistError)
from api.models import Accumulations, Targets
from api.serializers import (AccumulationCreateSerializer,
                             AccumulationInfoSerializer,
                             AccumulationSerializer,
                             AcumulationCategoriesSerializer,
                             ArchiveAccumulationCategorySerializer)

if TYPE_CHECKING:
    from django.db.models import QuerySet
    from rest_framework.request import Request


class TotalAmountAccumulationsGetAPI(APIView):
    """
    Return a total amount of user's accumulations.
    """

    permission_classes = (IsAuthenticated,)

    def get(self, request: Request) -> Response:
        total_sum = get_total_amount_of_accumulations(
            user=request.user
        )
        return Response(data={"total_sum": total_sum}, status=HTTP_200_OK)


class AccumulationsCategoriesListCreateAPI(ListCreateAPIView):
    """
    To get a list of user's accumulations categories and
    create a new accumulation category.
    """

    serializer_class = AcumulationCategoriesSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self) -> QuerySet[Targets]:
        return get_categories(
            user=self.request.user, category_model=Targets
        )


class AccumulationsCategoriesInfoAPI(RetrieveUpdateDestroyAPIView):
    """
    To get, update or remove a particular accumulation category.
    """

    serializer_class = AcumulationCategoriesSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self) -> QuerySet[Targets]:
        return get_categories(
            user=self.request.user, category_model=Targets
        )


class AccumulationsCategoriesArchiveAPI(APIView):
    """
    For archivation of target.
    To set set is_hidden=True in the particular Target instace.
    """

    serializer_class = ArchiveAccumulationCategorySerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request: Request, *args, **kwargs) -> Response:
        is_hidden = request.data.get("is_hidden")
        if not is_hidden:
            raise TypeError("Unexpected value")
        try:
            archive_accumulation_target(
                user=request.user,
                target_id=kwargs.get("pk")
            )
        except TargetDoesNotExistError:
            return Response(data="Target does not exist.", status=HTTP_404_NOT_FOUND)

        return Response(status=HTTP_202_ACCEPTED)


class AccumulationRetrieveUpdateDestroyAPI(RetrieveUpdateDestroyAPIView):
    """
    Provide the ability to retrieve, update or delete a model instance.
    """

    serializer_class = AccumulationSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = "pk"

    def get_queryset(self) -> QuerySet[Accumulations]:
        return get_accumulations(user=self.request.user)


class AccumulationCreateAPI(CreateAPIView):
    serializer_class = AccumulationCreateSerializer
    permission_classes = (IsAuthenticated,)


class LastAccumulationsGetAPI(ListAPIView):
    """
    To get a list of last user's accumulations.
    """

    serializer_class = AccumulationSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self) -> QuerySet[Accumulations]:
        """
        To get last user's accumulations.
        The amount of accumulations displayed is passed by the items parameter
        in the query parameters.
        """

        try:
            result = get_accumulations(
                user=self.request.user,
                number_of_items=self.request.GET.get("items")
            )
        except InvalidNumberOfItemsError:
            return

        return result


class AccumulationsInfoGetAPI(ListAPIView):
    serializer_class = AccumulationInfoSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self) -> QuerySet[Targets]:
        """
        To get information about user's accumulations.
        """

        result = get_accumulation_info(
            user=self.request.user
        )

        return result
