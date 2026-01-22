from rest_framework import viewsets
from .models import URLShortener
from .serializers import URLShortenerSerializer


class URLShortenerViewSet(viewsets.ModelViewSet):
    queryset = URLShortener.objects.all()
    serializer_class = URLShortenerSerializer
