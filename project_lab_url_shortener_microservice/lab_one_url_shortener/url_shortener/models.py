from datetime import timezone
from django.db import models
from django.conf import settings


class TagCategory(models.TextChoices):
    MARKETING = "Marketing", "Marketing"
    SOCIAL = "Social", "Social"
    NEWS = "News", "News"
    BLOG = "Blog", "Blog"
    E_COMMERCE = "E-Commerce", "E-Commerce"
    EDUCATION = "Education", "Education"
    ENTERTAINMENT = "Entertainment", "Entertainment"
    TECHNOLOGY = "Technology", "Technology"
    OTHER = "Other", "Other"


class Tag(models.Model):
    name = models.CharField(
        max_length=50,
        unique=True,
        choices=TagCategory.choices,
        default=TagCategory.OTHER,
    )

    def __str__(self):
        return self.name


class URLManager(models.Manager):
    def top_urls(self, limit=4):
        return self.order_by("-click_count")[:limit]

    def active(self):
        return self.filter(is_active=True)

    def expired_urls(self):
        return self.filter(expires_at__lte=timezone.now())


class URL(models.Model):
    original_url = models.URLField()
    short_code = models.CharField(max_length=10, unique=True, db_index=True)
    custom_alias = models.CharField(null=True, blank=True, unique=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="urls",
    )
    is_active = models.BooleanField(default=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    title = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    favicon = models.CharField(null=True, blank=True)
    click_count = models.PositiveIntegerField(default=0)
    tags = models.ManyToManyField(Tag, related_name="urls", blank=True)

    objects = URLManager()

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.short_code} -> {self.original_url}"


class UserClick(models.Model):
    url = models.ForeignKey(URL, on_delete=models.CASCADE, related_name="clicks")
    user_ip = models.GenericIPAddressField()
    city = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    clicked_at = models.DateTimeField(auto_now_add=True)
    user_agent = models.TextField()
    referrer = models.URLField(null=True, blank=True)

    def __str__(self):
        return (
            f"Click on {self.url.short_code} at {self.clicked_at} from {self.user_ip}"
        )
