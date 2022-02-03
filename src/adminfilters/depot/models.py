from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db import models


class StoredFilter(models.Model):
    name = models.CharField(blank=False, null=False, max_length=100)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    query_string = models.TextField(blank=True, null=True, default="")
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        ordering = ("name",)

    def __str__(self):
        return self.name
