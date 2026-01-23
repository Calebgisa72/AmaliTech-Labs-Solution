from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from .models import UserClick, URLShortener, models
from .serializers import URLShortenerSerializer, UserClickSerializer
from .services import UrlShortenerService
from .helpers import get_client_ip
from rest_framework.decorators import api_view


class URLShortenerView(APIView):
    def post(self, request):
        serializer = URLShortenerSerializer(data=request.data)
        if serializer.is_valid():
            original_url = serializer.validated_data["original_url"]  # type: ignore
            url_instance = UrlShortenerService.shorten_url(original_url)
            return Response(
                URLShortenerSerializer(url_instance).data,
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RedirectURLView(APIView):
    def get(self, request, short_code):
        url_instance = UrlShortenerService.get_original_url(short_code)

        user_ip = get_client_ip(request)
        UrlShortenerService.record_click(url_instance, user_ip)

        return HttpResponseRedirect(url_instance.original_url)


@api_view(["GET"])
def top_clicked_urls(request):
    top_urls = (
        UserClick.objects.values("url_shortener")
        .annotate(click_count=models.Count("url_shortener"))
        .order_by("-click_count")[:4]
    )

    results = []
    for item in top_urls:
        url = URLShortener.objects.get(pk=item["url_shortener"])
        results.append(
            {
                "short_code": url.short_code,
                "original_url": url.original_url,
                "clicks": item["click_count"],
            }
        )

    return Response(results, status=status.HTTP_200_OK)


@api_view(["GET"])
def get_user_clicks(request):
    user_ip = get_client_ip(request)
    user_clicks = UserClick.objects.filter(user_ip=user_ip)
    serializer = UserClickSerializer(user_clicks, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["DELETE"])
def delete_user_click(request, pk):
    user_click = get_object_or_404(UserClick, pk=pk)
    user_click.delete()
    return Response(
        {"message": "User click deleted successfully."},
        status=status.HTTP_204_NO_CONTENT,
    )
