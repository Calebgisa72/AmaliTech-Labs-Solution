from django.db import models

# Models are disabled as we migrated to Redis
# class URLShortener(models.Model):
#     original_url = models.URLField()
#     short_code = models.CharField(max_length=10, unique=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return f"{self.short_code} -> {self.original_url}"


# class UserClick(models.Model):
#     url_shortener = models.ForeignKey(URLShortener, on_delete=models.CASCADE)
#     user_ip = models.GenericIPAddressField()
#     clicked_at = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         unique_together = ("url_shortener", "user_ip")

#     def __str__(self):
#         return f"Click on {self.url_shortener.short_code} at {self.clicked_at} from {self.user_ip}"
