import uuid

from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models

from .managers import BaseManager


# Create your models here.
class BaseModel(models.Model):
    """
    Base model for all Target Database data models.
    All models should inherit from this to include the audit fields in them.
    Attributes:
        :param @id              :   primary key
        :param @created_at      :   timestamp of when the object is created.
        :param @updated_at      :   timestamp of when the object was last modified.
        :param @is_archived     :   status flag indicating if object should be visible or not.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    slug = models.SlugField(unique=True, db_index=True)
    created_at = models.DateTimeField(db_index=True, auto_now_add=True)
    updated_at = models.DateTimeField(db_index=True, auto_now=True)
    is_archived = models.BooleanField(default=False)
    metadata = models.JSONField(default=dict, null=True, blank=True)

    class Meta:
        abstract = True
        ordering = ("-updated_at", "-created_at")
