from django.db.models import TextChoices


class SupportedSites(TextChoices):
    """Supported sites for review scraping."""
    PLAY_STORE = "PS", "Play Store"

    def __str__(self):
        return self.value
