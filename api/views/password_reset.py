from __future__ import annotations

from typing import TYPE_CHECKING

from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view
from rest_framework.response import Response

if TYPE_CHECKING:
    from rest_framework.request import Request

@swagger_auto_schema(
    method='get',
    operation_id='Подтверждение восстановления пароля',
    operation_description='подтверждение восстановления пароля'
)
@api_view(http_method_names=["GET"])
def password_reset_api_controller(request: Request) -> Response:
    # """
    # подтверждение восстановления пароля
    # """
    uid = request.query_params.get("uid")
    token = request.query_params.get("token")
    data = {"uid": uid, "token": token}
    return Response(data=data)
