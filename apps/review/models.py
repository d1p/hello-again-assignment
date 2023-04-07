from django.db import models

from apps.review.types import SupportedSites


class ReviewURL(models.Model):
    url = models.URLField(max_length=200, unique=True)
    site = models.CharField(
        max_length=2,
        choices=SupportedSites.choices,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.url

    def save(self, *args, **kwargs):
        if "play.google.com" in self.url:
            self.site = SupportedSites.PLAY_STORE
        super().save(*args, **kwargs)


class Review(models.Model):
    review_url = models.ForeignKey(
        ReviewURL,
        on_delete=models.CASCADE,
        related_name="reviews",
    )

    user_name = models.CharField(max_length=60, blank=True, null=True)
    rating = models.SmallIntegerField(blank=True, null=True)
    review_text = models.TextField(blank=True, null=True)

    at = models.DateTimeField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class PlayStoreReview(Review):
    # set the default value to Play Store
    site = models.CharField(
        max_length=2,
        choices=SupportedSites.choices,
        default=SupportedSites.PLAY_STORE,
    )

    def __str__(self):
        return self.review_text