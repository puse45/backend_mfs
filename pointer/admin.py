from django.contrib import admin

# Register your models here.
from pointer.models import ClosestPointCompute


class ClosestPointAdmin(admin.ModelAdmin):
    list_display = (
        "points",
        "is_processing",
        "result",
        "is_done",
        "created_at",
        "updated_at",
    )
    search_fields = (
        "id",
        "points",
        "is_done",
        "is_processing",
    )
    list_per_page = 20


admin.site.register(ClosestPointCompute, ClosestPointAdmin)
