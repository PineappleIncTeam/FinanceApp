from __future__ import annotations
import requests
from typing import TYPE_CHECKING
from django.http import HttpResponseRedirect
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response

if TYPE_CHECKING:
    from rest_framework.request import Request


@api_view(http_method_names=["GET"])
def activate_users_api_controller(request: Request) -> Response:
    uid = request.query_params.get("uid")
    token = request.query_params.get("token")
    activation_data = {"uid": uid, "token": token}
    requests.post(
        url="http://" + settings.DOMAIN + "/api/v1/auth/users/activation/",
        data=activation_data
    )
    redirect_to = "http://" + settings.DOMAIN + "/api/v1/auth/token/login/"
    return HttpResponseRedirect(redirect_to=redirect_to)
