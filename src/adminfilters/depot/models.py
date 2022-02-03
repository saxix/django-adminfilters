from django.conf import settings
from django.db import models


class StoredFilter(models.Model):
    name = models.CharField(blank=False, null=False, max_length=100)
    query_string = models.TextField(blank=True, null=True, default="")
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
