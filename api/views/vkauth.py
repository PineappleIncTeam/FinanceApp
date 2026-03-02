import os
import logging
import time
import requests
import json
import uuid
import hashlib
import re
from dotenv import load_dotenv
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.cache import cache
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.test import APIRequestFactory
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.settings import api_settings as jwt_settings
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from api.views.vkchecktoken import VKCheckTokenView

logger = logging.getLogger(__name__)
load_dotenv()
User = get_user_model()


class VKOAuth2View(APIView):
    @swagger_auto_schema(
        operation_description="Обмен VK-кода на Django-совместимые токены и создание/обновление пользователя.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["code", "code_verifier", "device_id"],
            properties={
                "code": openapi.Schema(type=openapi.TYPE_STRING),
                "code_verifier": openapi.Schema(type=openapi.TYPE_STRING),
                "device_id": openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
        responses={
            200: openapi.Response(description="Успешно"),
            400: openapi.Response(description="Ошибка запроса"),
            500: openapi.Response(description="Ошибка сервера"),
        },
    )
    def post(self, request):
        request_id = str(uuid.uuid4())[:8]
        start_time = time.time()
        logger.info(f"[{request_id}] === НАЧАЛО ОБРАБОТКИ ЗАПРОСА VK OAuth ===")

        # Логирование IP клиента
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            client_ip = x_forwarded_for.split(',')[0]
        else:
            client_ip = request.META.get('REMOTE_ADDR')
        logger.info(f"[{request_id}] IP клиента: {client_ip}")

        try:
            # --- Шаг 1: Получение и проверка входных параметров ---
            code = request.data.get("code")
            code_verifier = request.data.get("code_verifier")
            device_id = request.data.get("device_id")

            # Безопасное хеширование code и code_verifier
            code_hash = hashlib.sha256(code.encode()).hexdigest() if code else None
            verifier_hash = hashlib.sha256(code_verifier.encode()).hexdigest() if code_verifier else None

            logger.info(f"[{request_id}] Получены параметры: code_hash={code_hash}, "
                        f"code_verifier_hash={verifier_hash}, device_id={device_id}")

            # Проверка формата code_verifier
            if code_verifier and not re.match(r'^[A-Za-z0-9-._~]{43,128}$', code_verifier):
                logger.warning(f"[{request_id}] code_verifier не соответствует требованиям: длина={len(code_verifier)}")

            # Проверка на повторное использование кода
            if code_hash and cache.get(f"used_code:{code_hash}"):
                logger.warning(f"[{request_id}] Обнаружен повторный запрос с тем же code (hash={code_hash})")
            else:
                # Сохраняем код в кэш на 60 секунд для предотвращения повторного использования
                cache.set(f"used_code:{code_hash}", True, timeout=60)

            if not code or not code_verifier or not device_id:
                missing = [k for k, v in [('code', code), ('code_verifier', code_verifier), ('device_id', device_id)] if not v]
                logger.warning(f"[{request_id}] Ошибка: отсутствуют обязательные параметры: {missing}")
                logger.info(f"[{request_id}] Ответ 400: отсутствуют параметры")
                return Response({"error": "Missing parameters"}, status=status.HTTP_400_BAD_REQUEST)

            logger.info(f"[{request_id}] Все обязательные параметры присутствуют")

            # --- Шаг 2: Определение redirect_uri ---
            # redirect_uri = os.getenv("REDIRECT_URI")
            redirect_uri = "https://dev.freenance.space/profitMoney"
            if not redirect_uri:
                redirect_uri = "https://dev.freenance.space/api/v1/vkauth/"
                logger.warning(f"[{request_id}] REDIRECT_URI не задан, используется значение по умолчанию: {redirect_uri}")
            else:
                logger.info(f"[{request_id}] Используется redirect_uri: {redirect_uri}")

            # --- Шаг 3: Обмен кода на токены через VK ---
            logger.info(f"[{request_id}] ЭТАП 1: Запрос токена у VK (обмен кода)")
            vk_token_url = "https://id.vk.com/oauth2/auth"
            logger.info(f"[{request_id}] URL запроса к VK: {vk_token_url}")

            payload = {
                "grant_type": "authorization_code",
                "code": code,
                "code_verifier": code_verifier,
                "device_id": device_id,
                "client_id": os.getenv("CLIENT_ID"),
                "client_secret": os.getenv("CL_SECRET"),
                "redirect_uri": redirect_uri,
            }

            # Логируем параметры запроса (без client_secret)
            log_payload = payload.copy()
            log_payload.pop("client_secret", None)
            logger.info(f"[{request_id}] Параметры запроса к VK: {json.dumps(log_payload, ensure_ascii=False)}")

            start_vk = time.time()
            try:
                vk_response = requests.post(vk_token_url, data=payload, timeout=5)
            except requests.RequestException as e:
                logger.error(f"[{request_id}] Ошибка соединения с VK при запросе токена", exc_info=True)
                logger.info(f"[{request_id}] Ответ 500: не удалось соединиться с VK")
                return Response({"error": "Failed to reach VK token endpoint"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            vk_duration = time.time() - start_vk
            logger.info(f"[{request_id}] Запрос к VK выполнен за {vk_duration:.2f} сек, статус ответа: {vk_response.status_code}")

            # Логируем заголовки ответа VK
            logger.info(f"[{request_id}] Заголовки ответа VK: {dict(vk_response.headers)}")

            # Пытаемся распарсить JSON ответа, при ошибке логируем текст
            try:
                response_json = vk_response.json()
                logger.info(f"[{request_id}] JSON ответа от VK успешно разобран")
            except ValueError:
                logger.error(f"[{request_id}] Не удалось разобрать JSON ответа VK. Тело ответа: {vk_response.text}")
                logger.info(f"[{request_id}] Ответ 500: некорректный JSON от VK")
                return Response({"error": "Invalid JSON from VK"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            # Логируем полный ответ VK (даже если это ошибка)
            logger.info(f"[{request_id}] Ответ VK: {json.dumps(response_json, ensure_ascii=False)}")

            if vk_response.status_code != 200:
                logger.error(f"[{request_id}] VK вернул ошибку: {vk_response.status_code}, тело: {vk_response.text}")
                logger.info(f"[{request_id}] Проксируем ответ VK клиенту с кодом {vk_response.status_code}")
                return Response(response_json, status=vk_response.status_code)

            tokens = response_json
            access_token = tokens.get("access_token")
            refresh_token_vk = tokens.get("refresh_token")
            expires_in = tokens.get("expires_in")

            if not access_token:
                logger.error(f"[{request_id}] В ответе VK отсутствует access_token. Полный ответ: {json.dumps(tokens, ensure_ascii=False)}")
                logger.info(f"[{request_id}] Ответ 403: токен доступа не получен")
                return Response({"error": "No access token received"}, status=status.HTTP_403_FORBIDDEN)

            logger.info(f"[{request_id}] Токен доступа VK успешно получен, expires_in={expires_in}")
            if refresh_token_vk:
                logger.info(f"[{request_id}] Получен refresh_token VK")
            else:
                logger.info(f"[{request_id}] Refresh_token VK отсутствует")

            # --- Шаг 4: Валидация токена через VKCheckTokenView ---
            logger.info(f"[{request_id}] ЭТАП 2: Валидация токена через VKCheckTokenView")
            factory = APIRequestFactory()
            check_req = factory.post("/api/v1/vk/check-token/", {"token": access_token}, format="json")
            check_view = VKCheckTokenView.as_view()

            start_check = time.time()
            try:
                check_response = check_view(check_req)
                check_duration = time.time() - start_check
                logger.info(f"[{request_id}] Валидация токена выполнена за {check_duration:.2f} сек")
            except Exception as exc:
                logger.exception(f"[{request_id}] Исключение при вызове VKCheckTokenView: {exc}")
                logger.info(f"[{request_id}] Ответ 500: ошибка валидации токена")
                return Response({"error": "server_error", "error_description": "Token validation failed"},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            if getattr(check_response, "status_code", None) != 200:
                logger.error(f"[{request_id}] Валидация токена не пройдена. Статус: {check_response.status_code}, данные: {getattr(check_response, 'data', None)}")
                logger.info(f"[{request_id}] Ответ 403: токен недействителен")
                return Response({"error": "invalid_token", "detail": getattr(check_response, "data", None)},
                                status=status.HTTP_403_FORBIDDEN)

            logger.info(f"[{request_id}] Токен успешно валидирован")

            # --- Шаг 5: Получение информации о пользователе ---
            logger.info(f"[{request_id}] ЭТАП 3: Запрос информации о пользователе")
            user_info_url = "https://id.vk.com/oauth2/user_info"
            user_info_payload = {"access_token": access_token, "client_id": os.getenv("CLIENT_ID")}

            start_user = time.time()
            try:
                user_info_response = requests.post(user_info_url, data=user_info_payload, timeout=5)
            except requests.RequestException as e:
                logger.error(f"[{request_id}] Ошибка соединения с VK при запросе данных пользователя", exc_info=True)
                logger.info(f"[{request_id}] Ответ 500: не удалось получить данные пользователя")
                return Response({"error": "Failed to fetch user info"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            user_duration = time.time() - start_user
            logger.info(f"[{request_id}] Запрос данных пользователя выполнен за {user_duration:.2f} сек, статус ответа: {user_info_response.status_code}")

            if user_info_response.status_code != 200:
                logger.error(f"[{request_id}] VK вернул ошибку при запросе user_info: {user_info_response.status_code}, тело: {user_info_response.text}")
                logger.info(f"[{request_id}] Проксируем ответ VK клиенту с кодом {user_info_response.status_code}")
                return Response(user_info_response.json(), status=user_info_response.status_code)

            try:
                vk_user = user_info_response.json()
                logger.info(f"[{request_id}] JSON данных пользователя успешно разобран")
            except ValueError as e:
                logger.error(f"[{request_id}] Не удалось разобрать JSON данных пользователя: {user_info_response.text}", exc_info=True)
                logger.info(f"[{request_id}] Ответ 500: некорректный JSON от VK")
                return Response({"error": "Invalid user info JSON"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            vk_id = vk_user.get("sub") or vk_user.get("id")
            first_name = vk_user.get("first_name", "")
            last_name = vk_user.get("last_name", "")
            email = vk_user.get("email") or f"{vk_id}@vk.local"
            avatar = vk_user.get("picture")

            logger.info(f"[{request_id}] Получены данные пользователя: VK ID={vk_id}, имя={first_name}, фамилия={last_name}, email={email}, аватар={'есть' if avatar else 'нет'}")

            # --- Шаг 6: Создание или обновление пользователя в БД ---
            logger.info(f"[{request_id}] ЭТАП 4: Создание/обновление пользователя")
            username = f"vk_{vk_id}" if vk_id else None

            try:
                user, created = User.objects.get_or_create(
                    username=username,
                    defaults={
                        "first_name": first_name,
                        "last_name": last_name,
                        "email": email,
                    },
                )
                if created:
                    logger.info(f"[{request_id}] Создан новый пользователь: id={user.id}, vk_id={vk_id}")
                else:
                    # Обновляем данные, если они изменились
                    updated = False
                    if user.first_name != first_name:
                        user.first_name = first_name
                        updated = True
                    if user.last_name != last_name:
                        user.last_name = last_name
                        updated = True
                    if user.email != email:
                        user.email = email
                        updated = True
                    if updated:
                        user.save()
                        logger.info(f"[{request_id}] Данные пользователя id={user.id} обновлены")
                    else:
                        logger.info(f"[{request_id}] Пользователь id={user.id} уже существует, данные актуальны")
            except Exception as e:
                logger.error(f"[{request_id}] Ошибка при создании/обновлении пользователя с vk_id={vk_id}", exc_info=True)
                logger.info(f"[{request_id}] Ответ 500: не удалось создать/обновить пользователя")
                return Response({"error": "user_creation_failed"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            # --- Шаг 7: Генерация JWT токенов ---
            logger.info(f"[{request_id}] ЭТАП 5: Генерация JWT токенов")
            refresh = RefreshToken.for_user(user)
            access_token_jwt = str(refresh.access_token)
            refresh_token_jwt = str(refresh)
            logger.info(f"[{request_id}] JWT токены сгенерированы для пользователя id={user.id}")

            # --- Шаг 8: Формирование ответа и установка кук ---
            logger.info(f"[{request_id}] ЭТАП 6: Установка cookie")
            response_data = {
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "avatar": avatar,
                }
            }
            resp = Response(response_data, status=status.HTTP_200_OK)

            # Определяем время жизни кук
            try:
                access_lifetime = jwt_settings.ACCESS_TOKEN_LIFETIME
                refresh_lifetime = jwt_settings.REFRESH_TOKEN_LIFETIME
                access_max_age = int(access_lifetime.total_seconds())
                refresh_max_age = int(refresh_lifetime.total_seconds())
            except Exception:
                access_max_age = 3600
                refresh_max_age = 60 * 60 * 24 * 7
                logger.warning(f"[{request_id}] Не удалось получить время жизни JWT из настроек, используются значения по умолчанию: access={access_max_age}с, refresh={refresh_max_age}с")

            secure_flag = not getattr(settings, "DEBUG", False)

            resp.set_cookie("jwt_access", access_token_jwt, httponly=True, secure=secure_flag,
                            samesite="Lax", max_age=access_max_age, path="/")
            resp.set_cookie("jwt_refresh", refresh_token_jwt, httponly=True, secure=secure_flag,
                            samesite="Lax", max_age=refresh_max_age, path="/")
            resp.set_cookie("vk_access", access_token, httponly=True, secure=secure_flag,
                            samesite="Lax", max_age=int(tokens.get("expires_in", access_max_age)), path="/")
            if refresh_token_vk:
                resp.set_cookie("vk_refresh", refresh_token_vk, httponly=True, secure=secure_flag,
                                samesite="Lax", max_age=int(tokens.get("expires_in", refresh_max_age)), path="/")

            logger.info(f"[{request_id}] Установлены cookie: jwt_access, jwt_refresh, vk_access" +
                        (", vk_refresh" if refresh_token_vk else ""))

            # --- Шаг 9: Кэширование токенов ---
            logger.info(f"[{request_id}] ЭТАП 7: Кэширование токенов")
            try:
                vk_ttl = tokens.get("expires_in") or access_max_age
                cache.set(f"vk_tokens:{vk_id}", tokens, timeout=int(vk_ttl))
                cache.set(f"jwt_tokens:{user.id}", {"access": access_token_jwt, "refresh": refresh_token_jwt},
                          timeout=refresh_max_age)
                logger.info(f"[{request_id}] Токены закэшированы для пользователя id={user.id}, VK TTL={vk_ttl}с")
            except Exception as e:
                logger.warning(f"[{request_id}] Не удалось закэшировать токены: {e}", exc_info=True)

            # --- Шаг 10: Завершение ---
            duration = time.time() - start_time
            logger.info(f"[{request_id}] === УСПЕШНОЕ ЗАВЕРШЕНИЕ OAuth для пользователя id={user.id}, общее время: {duration:.2f} сек ===")
            return resp

        except Exception as e:
            # Любое необработанное исключение
            logger.exception(f"[{request_id}] НЕОБРАБОТАННОЕ ИСКЛЮЧЕНИЕ в VKOAuth2View")
            logger.info(f"[{request_id}] Ответ 500: внутренняя ошибка сервера")
            return Response({"error": "internal_server_error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)