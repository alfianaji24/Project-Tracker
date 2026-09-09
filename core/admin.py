from django.contrib import admin, messages
from django.db.models import Count
from django.utils.formats import localize
from django.utils.translation import gettext_lazy as _

from core.models import (
    ContractType,
    Customer,
    Project,
    ProjectStatus,
    ProjectType,
    TOP,
    Vendor,
)


class ProtectedMasterAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "status", "updated_at")
    list_filter = ("status",)
    search_fields = ("code", "name")
    readonly_fields = ("created_at", "updated_at")

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if hasattr(self.model, "projects"):
            return qs.annotate(_project_count=Count("projects"))
        return qs

    def delete_model(self, request, obj):
        if hasattr(obj, "projects") and obj.projects.exists():
            self.message_user(
                request,
                _("Data master yang sudah digunakan project tidak boleh dihapus. Nonaktifkan saja."),
                level=messages.ERROR,
            )
            return
        super().delete_model(request, obj)

    def delete_queryset(self, request, queryset):
        blocked = queryset.filter(projects__isnull=False).distinct()
        if blocked.exists():
            self.message_user(
                request,
                _("Beberapa data master sudah digunakan project dan tidak dapat dihapus."),
                level=messages.ERROR,
            )
            queryset = queryset.exclude(pk__in=blocked.values_list("pk", flat=True))
        if queryset.exists():
            super().delete_queryset(request, queryset)


@admin.register(Customer)
class CustomerAdmin(ProtectedMasterAdmin):
    list_display = ("code", "name", "phone", "email", "status", "updated_at")
    search_fields = ("code", "name", "email", "phone")

    def delete_model(self, request, obj):
        if obj.projects.exists():
            self.message_user(
                request,
                _("Customer yang sudah digunakan project tidak boleh dihapus. Nonaktifkan saja."),
                level=messages.ERROR,
            )
            return
        super().delete_model(request, obj)


@admin.register(Vendor)
class VendorAdmin(ProtectedMasterAdmin):
    list_display = ("code", "name", "phone", "email", "status", "updated_at")
    search_fields = ("code", "name", "email", "phone")

    def delete_model(self, request, obj):
        if obj.projects.exists():
            self.message_user(
                request,
                _("Vendor yang sudah digunakan project tidak boleh dihapus. Nonaktifkan saja."),
                level=messages.ERROR,
            )
            return
        super().delete_model(request, obj)


@admin.register(ContractType)
class ContractTypeAdmin(ProtectedMasterAdmin):
    pass


@admin.register(ProjectType)
class ProjectTypeAdmin(ProtectedMasterAdmin):
    pass


@admin.register(TOP)
class TOPAdmin(ProtectedMasterAdmin):
    list_display = ("code", "name", "description", "status", "updated_at")


@admin.register(ProjectStatus)
class ProjectStatusAdmin(ProtectedMasterAdmin):
    pass


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        "project_code",
        "project_name",
        "customer",
        "vendor",
        "contract_type",
        "project_type",
        "contract_start_date",
        "contract_end_date",
        "formatted_work_value",
        "project_status",
        "status",
    )
    list_filter = (
        "customer",
        "vendor",
        "contract_type",
        "project_type",
        "top",
        "project_status",
        "status",
        "contract_start_date",
        "contract_end_date",
    )
    search_fields = (
        "project_code",
        "project_name",
        "customer__name",
        "customer__code",
        "vendor__name",
        "vendor__code",
    )
    autocomplete_fields = (
        "customer",
        "vendor",
        "contract_type",
        "project_type",
        "top",
        "project_status",
    )
    readonly_fields = ("created_at", "updated_at", "formatted_work_value")
    date_hierarchy = "contract_start_date"
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "project_code",
                    "project_name",
                    "project_status",
                    "status",
                )
            },
        ),
        (
            _("Relations"),
            {
                "fields": (
                    "customer",
                    "vendor",
                    "contract_type",
                    "project_type",
                    "top",
                )
            },
        ),
        (
            _("Contract"),
            {
                "fields": (
                    "contract_start_date",
                    "contract_end_date",
                    "work_value",
                    "formatted_work_value",
                )
            },
        ),
        (
            _("Audit"),
            {"fields": ("created_at", "updated_at")},
        ),
    )

    @admin.display(description=_("Work Value"))
    def formatted_work_value(self, obj):
        if obj.work_value is None:
            return "-"
        return f"Rp {localize(obj.work_value)}"
