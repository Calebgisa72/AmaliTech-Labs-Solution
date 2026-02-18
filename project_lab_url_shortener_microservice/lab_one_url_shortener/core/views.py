from rest_framework.throttling import ScopedRateThrottle
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from drf_spectacular.utils import extend_schema
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import RegisterSerializer


class RegisterView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        request=RegisterSerializer,
        responses={201: RegisterSerializer},
        description="Register a new user",
    )
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomTokenObtainPairView(TokenObtainPairView):
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "login"


class HealthCheckView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        from django.db import connections
        from django.db.utils import OperationalError
        from url_shortener.redis_client import get_redis_client
        from redis.exceptions import ConnectionError

        health = {"status": "ok", "components": {"db": "healthy", "redis": "healthy"}}
        status_code = status.HTTP_200_OK

        # Check DB
        try:
            connections["default"].cursor()
        except OperationalError:
            health["components"]["db"] = "unhealthy"
            health["status"] = "unavailable"
            status_code = status.HTTP_503_SERVICE_UNAVAILABLE

        # Check Redis
        try:
            redis_client = get_redis_client()
            redis_client.ping()
        except ConnectionError:
            health["components"]["redis"] = "unhealthy"
            health["status"] = "unavailable"
            status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        except Exception:
            health["components"]["redis"] = "unhealthy"
            health["status"] = "unavailable"
            status_code = status.HTTP_503_SERVICE_UNAVAILABLE

        return Response(health, status=status_code)
