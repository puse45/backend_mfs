import os

from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from base.models import BaseModel, StatusModel

# Create your models here.


class ClosestPointCompute(BaseModel, StatusModel):
    points = ArrayField(ArrayField(models.FloatField(null=False, blank=False)))
    result = models.JSONField(default=dict, blank=False, null=False)
    slug = False

    def __unicode__(self):
        return "Closest Point Compute"

    class Meta:
        ordering = ("-created_at",)
        get_latest_by = ("-created_at",)
        verbose_name = _("Closest Point Compute")
        verbose_name_plural = _("Closest Point Computes")

    def __str__(self):
        return f"{self.points} - {self.created_at}"
