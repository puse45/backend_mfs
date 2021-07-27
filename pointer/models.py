import os

from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from base.models import BaseModel, StatusModel

# Create your models here.


def upload_dir(instance, filename):
    f_name, ext = os.path.splitext(filename)
    folder = os.path.join("point", str(instance._meta.model_name), str(instance))
    return os.path.join(folder, str(timezone.now())[:19] + ext)


class ClosestPointBatchCompute(BaseModel, StatusModel):
    csv_file = models.FileField(upload_to=upload_dir, blank=False, null=False)
    column_a = models.CharField(max_length=100, blank=False, null=False)
    column_b = models.CharField(max_length=100, blank=False, null=False)
    computation_result = models.CharField(max_length=200, blank=False, null=False)
    slug = False

    def __unicode__(self):
        return "Closest Point Batch Compute"

    class Meta:
        ordering = ("-created_at",)
        get_latest_by = ("-created_at",)
        verbose_name = _("Closest Point Batch Compute")
        verbose_name_plural = _("Closest Point Batch Computes")

    def __str__(self):
        return f"{self.csv_file} - {self.created_at}"


class ClosestPointCompute(BaseModel, StatusModel):
    points = models.TextField(blank=False, null=False)
    computation_result = models.CharField(max_length=200, blank=False, null=False)
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
