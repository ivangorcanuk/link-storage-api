from django.db import models
from django.contrib.auth import get_user_model
from LinkHub.links.models import Link

User = get_user_model()


class Collection(models.Model):
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='collections'
    )
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    links = models.ManyToManyField(
        Link,
        related_name='collections',
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ['owner', 'name']

    def __str__(self):
        return f"{self.name} (by {self.owner.email})"