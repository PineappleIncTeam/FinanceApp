import requests
from django.http import HttpResponse, JsonResponse
from django.utils.deprecation import MiddlewareMixin

class RefreshTokenMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        if response.status_code == 401:
            refresh_token = request.COOKIES.get('refresh_token')

            if refresh_token:
                try:
                    refresh_url = 'https://dev.freenance.store/api/v1/auth/refresh/'
                    refresh_response = requests.post(
                        refresh_url,
                        cookies={'refresh_token': refresh_token},
                        auth=None
                    )

                    if refresh_response.status_code == 200:
                        new_access = refresh_response.json().get('access')

                        original_url = request.build_absolute_uri()
                        method = request.method.upper()
                        headers = {
                            'Authorization': f'Bearer {new_access}',
                            'Content-Type': request.headers.get('Content-Type', 'application/json')
                        }
                        body = request.body if method in ['POST', 'PUT', 'PATCH', 'DELETE'] else None

                        retry_response = requests.request(
                            method=method,
                            url=original_url,
                            headers=headers,
                            data=body,
                            cookies=request.COOKIES
                        )

                        django_response = HttpResponse(
                            content=retry_response.content,
                            status=retry_response.status_code,
                            content_type=retry_response.headers.get('Content-Type', 'application/json')
                        )

                        django_response.set_cookie(
                            key='access_token',
                            value=new_access,
                            httponly=True,
                            secure=True,
                            samesite='Strict',
                            max_age=300
                        )

                        return django_response
                    else:
                        print("⚠️ Ответ от refresh: ", refresh_response.status_code)
                        print("📦 Тело: ", refresh_response.text)
                        return JsonResponse({"error": "Token refresh failed", "тело": refresh_response.text}, status=refresh_response.status_code)


                except Exception as e:
                    return JsonResponse({"error": str(e)}, status=500)

        return response
