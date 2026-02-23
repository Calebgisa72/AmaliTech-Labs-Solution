from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import httpx
from bs4 import BeautifulSoup
from drf_spectacular.utils import extend_schema, OpenApiParameter


class PreviewView(APIView):
    """
    A minimal API View that takes a URL as a query parameter and
    scrapes it for title, description, and favicon.
    """

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="url",
                description="The URL to scrape",
                required=True,
                type=str,
            )
        ],
        responses={200: dict, 400: dict, 404: dict, 500: dict},
        description="Scrape URL for preview metadata",
    )
    def get(self, request):
        target_url = request.query_params.get("url")

        if not target_url:
            return Response(
                {"error": "Missing 'url' query parameter."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            with httpx.Client(timeout=5.0) as client:
                response = client.get(target_url, follow_redirects=True)
                response.raise_for_status()

                soup = BeautifulSoup(response.text, "html.parser")

                # Extract title
                title = ""
                if soup.title and soup.title.string:
                    title = soup.title.string.strip()

                # Extract description
                description = ""
                meta_desc = soup.find("meta", attrs={"name": "description"})
                if meta_desc and meta_desc.get("content"):
                    description = meta_desc["content"].strip()

                # Extract favicon
                favicon = ""
                icon_link = soup.find("link", rel=lambda x: x and "icon" in x.lower())
                if icon_link and icon_link.get("href"):
                    favicon = icon_link["href"].strip()
                    # Handle relative URLs for favicon
                    if not favicon.startswith("http"):
                        from urllib.parse import urljoin

                        favicon = urljoin(str(response.url), favicon)

                return Response(
                    {
                        "title": title,
                        "description": description,
                        "favicon": favicon,
                    },
                    status=status.HTTP_200_OK,
                )

        except httpx.RequestError as e:
            return Response(
                {"error": f"Failed to fetch the URL: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            return Response(
                {"error": f"An unexpected error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
