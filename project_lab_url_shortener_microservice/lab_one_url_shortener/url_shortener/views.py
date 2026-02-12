from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponseRedirect, Http404
from .serializers import URLSerializer
from .services import UrlShortenerService
from .helpers import get_client_ip
from rest_framework.decorators import api_view
from drf_spectacular.utils import extend_schema
from .repositories import URLRepository
from rest_framework.permissions import IsAuthenticated
from core.permissions import IsOwnerOrReadOnly


class URLView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=URLSerializer,
        responses={201: URLSerializer},
        description="Shorten a URL",
    )
    def post(self, request):
        serializer = URLSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            if user.tier == "Free":
                active_count = URLRepository().count_active_urls(user)
                if active_count >= 10:
                    return Response(
                        {
                            "message": "Free users are limited to 10 active URLs. Upgrade to Premium for unlimited URLs."
                        },
                        status=status.HTTP_403_FORBIDDEN,
                    )

                if serializer.validated_data.get("custom_alias"):
                    return Response(
                        {
                            "message": "Custom aliases are only available for Premium users."
                        },
                        status=status.HTTP_403_FORBIDDEN,
                    )

            repo = URLRepository()
            service = UrlShortenerService(repo)

            result = service.shorten_url(
                **serializer.validated_data,
                owner=request.user,
            )
            return Response(
                result,
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RedirectURLView(APIView):
    def get(self, request, identifier):
        repo = URLRepository()
        service = UrlShortenerService(repo)
        url_data = service.get_original_url(identifier)
        if not url_data:
            return Response(
                {"message": "URL not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        expires_at = url_data.get("expires_at")
        if expires_at and expires_at < timezone.now():
            raise Http404("URL has expired")

        if not url_data.get("is_active"):
            raise Http404("URL is no longer active")

        user_ip = get_client_ip(request)
        user_agent = request.META.get("HTTP_USER_AGENT", "")
        referrer = request.META.get("HTTP_REFERER", "")
        city = request.query_params.get("city")
        country = request.query_params.get("country")
        service.record_click(
            identifier=identifier,
            user_ip=user_ip,
            user_agent=user_agent,
            referrer=referrer,
            city=city,
            country=country,
        )

        return HttpResponseRedirect(url_data["original_url"])


class URLDetailView(APIView):
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    @extend_schema(
        request=URLSerializer,
        responses={200: URLSerializer},
        description="Update a URL",
    )
    def put(self, request, identifier):
        repo = URLRepository()
        obj = repo.get_by_short_code_or_custom_alias(identifier)
        if not obj:
            return Response(
                {"message": "URL not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        self.check_object_permissions(request, obj)
        serializer = URLSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            # Check tier limits for updates
            if request.user.tier == "Free":
                if "custom_alias" in serializer.validated_data:
                    return Response(
                        {"message": "Free users cannot set or update custom aliases."},
                        status=status.HTTP_403_FORBIDDEN,
                    )

            service = UrlShortenerService(repo)

            result = service.update_url(
                obj,
                serializer.validated_data,
            )
            return Response(result, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        responses={200: URLSerializer},
        description="Delete a URL",
    )
    def delete(self, request, identifier):
        repo = URLRepository()
        obj = repo.get_by_short_code_or_custom_alias(identifier)
        if not obj:
            return Response(
                {"message": "URL not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        self.check_object_permissions(request, obj)
        service = UrlShortenerService(repo)

        result = service.delete_url(obj)
        if result:
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(["GET"])
def top_clicked_urls(request):
    repo = URLRepository()
    service = UrlShortenerService(repo)
    results = service.get_top_clicked()
    return Response(results, status=status.HTTP_200_OK)


@api_view(["GET"])
def get_user_clicks(request):
    user_ip = get_client_ip(request)
    repo = URLRepository()
    service = UrlShortenerService(repo)
    results = service.get_user_clicks(user_ip)
    return Response(results, status=status.HTTP_200_OK)
