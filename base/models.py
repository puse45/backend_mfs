import uuid

from django.db import models


# Create your models here.
class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    slug = models.SlugField(unique=True, db_index=True)
    created_at = models.DateTimeField(db_index=True, auto_now_add=True)
    updated_at = models.DateTimeField(db_index=True, auto_now=True)
    metadata = models.JSONField(default=dict, null=True, blank=True)

    class Meta:
        abstract = True
        ordering = ("-updated_at", "-created_at")


class StatusModel(models.Model):
    is_processing = models.BooleanField(default=False)
    is_done = models.BooleanField(default=False)

    class Meta:
        abstract = True
        ordering = ("-is_processing", "-is_done")
