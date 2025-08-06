import json
import requests
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin


def process_response(request, response):
    if response.status_code == 401:
        refresh_token = request.COOKIES.get('refresh_token')

        if refresh_token:
            refresh_url = 'https://dev.freenance.store/api/v1/auth/refresh/'
            refresh_response = requests.post(refresh_url, data={
                'refresh': refresh_token
            })

            if refresh_response.status_code == 200:
                new_access = refresh_response.json().get('access')

                new_response = JsonResponse({'access': new_access})
                new_response.set_cookie(
                    key='access_token',
                    value=new_access,
                    httponly=True,
                    secure=True,
                    samesite='Strict',
                    max_age=5 * 60
                )
                return new_response

    return response

