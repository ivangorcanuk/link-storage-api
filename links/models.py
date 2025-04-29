from django.db import models
from django.contrib.auth import get_user_model
from enum import Enum

User = get_user_model()


class LinkType(Enum):
    WEBSITE = 'website'
    BOOK = 'book'
    ARTICLE = 'article'
    MUSIC = 'music'
    VIDEO = 'video'

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]


class Link(models.Model):
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='links'
    )
    url = models.URLField(max_length=2048)
    title = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    image_url = models.URLField(max_length=2048, blank=True)
    link_type = models.CharField(
        max_length=20,
        choices=LinkType.choices(),
        default=LinkType.WEBSITE.value
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['owner', 'url']
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} ({self.url})"