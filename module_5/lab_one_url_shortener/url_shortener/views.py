from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponseRedirect, Http404
from .serializers import URLShortenerSerializer
from .services import UrlShortenerService
from .helpers import get_client_ip
from rest_framework.decorators import api_view
from drf_spectacular.utils import extend_schema


class URLShortenerView(APIView):
    @extend_schema(
        request=URLShortenerSerializer,
        responses={201: URLShortenerSerializer},
        description="Shorten a URL",
    )
    def post(self, request):
        serializer = URLShortenerSerializer(data=request.data)
        if serializer.is_valid():
            original_url = serializer.validated_data["original_url"]  # type: ignore
            result = UrlShortenerService.shorten_url(original_url)
            return Response(
                result,
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RedirectURLView(APIView):
    def get(self, request, short_code):
        url_data = UrlShortenerService.get_original_url(short_code)
        if not url_data:
            raise Http404("Short URL not found")

        user_ip = get_client_ip(request)
        UrlShortenerService.record_click(short_code, url_data["original_url"], user_ip)

        return HttpResponseRedirect(url_data["original_url"])


@api_view(["GET"])
def top_clicked_urls(request):
    results = UrlShortenerService.get_top_clicked()
    return Response(results, status=status.HTTP_200_OK)


@api_view(["GET"])
def get_user_clicks(request):
    user_ip = get_client_ip(request)
    results = UrlShortenerService.get_user_clicks(user_ip)
    return Response(results, status=status.HTTP_200_OK)
