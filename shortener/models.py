from django.db import models
from django.utils.crypto import get_random_string

class URL(models.Model):
    original_url = models.URLField()
    shortened_url = models.CharField(
        max_length=10,
        unique=True,
        default=lambda: get_random_string(length=2)
    )

    def __str__(self):
        return f"{self.original_url} -> {self.shortened_url}"

    def get_absolute_url(self):
        return f"/r/{self.shortened_url}/"
    