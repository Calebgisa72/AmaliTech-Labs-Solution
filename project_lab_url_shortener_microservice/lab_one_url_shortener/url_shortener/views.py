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


class URLView(APIView):
    @extend_schema(
        request=URLSerializer,
        responses={201: URLSerializer},
        description="Shorten a URL",
    )
    def post(self, request):
        serializer = URLSerializer(data=request.data)
        if serializer.is_valid():
            original_url: str = serializer.validated_data.get("original_url")
            custom_alias: str | None = serializer.validated_data.get("custom_alias")
            expires_at: str | None = serializer.validated_data.get("expires_at")
            title: str | None = serializer.validated_data.get("title")
            description: str | None = serializer.validated_data.get("description")
            favicon: str | None = serializer.validated_data.get("favicon")
            tags: list | None = serializer.validated_data.get("tags")
            user = request.user if request.user.is_authenticated else None

            repo = URLRepository()
            service = UrlShortenerService(repo)

            result = service.shorten_url(
                original_url,
                user,
                custom_alias,
                expires_at,
                title,
                description,
                favicon,
                tags,
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
            raise Http404("URL not found")

        if url_data.expires_at and url_data.expires_at < timezone.now():
            raise Http404("URL has expired")

        if not url_data.is_active:
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

        return HttpResponseRedirect(url_data.original_url)


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
