from decimal import Decimal

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from core.validators import validate_business_code


class ActiveStatus(models.TextChoices):
    ACTIVE = "active", _("Active")
    INACTIVE = "inactive", _("Inactive")


class TimestampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class MasterModel(TimestampedModel):
    code = models.CharField(
        max_length=4,
        unique=True,
        validators=[validate_business_code],
        verbose_name=_("Code"),
    )
    name = models.CharField(max_length=255, verbose_name=_("Name"))
    status = models.CharField(
        max_length=8,
        choices=ActiveStatus.choices,
        default=ActiveStatus.ACTIVE,
        verbose_name=_("Status"),
    )

    class Meta:
        abstract = True
        ordering = ["code"]

    def __str__(self) -> str:
        return f"{self.code} - {self.name}"


class Customer(TimestampedModel):
    code = models.CharField(
        max_length=4,
        unique=True,
        validators=[validate_business_code],
        verbose_name=_("Customer Code"),
    )
    name = models.CharField(max_length=255, verbose_name=_("Customer Name"))
    address = models.TextField(blank=True, verbose_name=_("Address"))
    phone = models.CharField(max_length=50, blank=True, verbose_name=_("Phone"))
    email = models.EmailField(blank=True, verbose_name=_("Email"))
    status = models.CharField(
        max_length=8,
        choices=ActiveStatus.choices,
        default=ActiveStatus.ACTIVE,
        verbose_name=_("Status"),
    )

    class Meta:
        ordering = ["code"]
        verbose_name = _("Customer")
        verbose_name_plural = _("Customers")

    def __str__(self) -> str:
        return f"{self.code} - {self.name}"


class Vendor(TimestampedModel):
    code = models.CharField(
        max_length=4,
        unique=True,
        validators=[validate_business_code],
        verbose_name=_("Vendor Code"),
    )
    name = models.CharField(max_length=255, verbose_name=_("Vendor Name"))
    address = models.TextField(blank=True, verbose_name=_("Address"))
    phone = models.CharField(max_length=50, blank=True, verbose_name=_("Phone"))
    email = models.EmailField(blank=True, verbose_name=_("Email"))
    status = models.CharField(
        max_length=8,
        choices=ActiveStatus.choices,
        default=ActiveStatus.ACTIVE,
        verbose_name=_("Status"),
    )

    class Meta:
        ordering = ["code"]
        verbose_name = _("Vendor")
        verbose_name_plural = _("Vendors")

    def __str__(self) -> str:
        return f"{self.code} - {self.name}"


class ContractType(MasterModel):
    class Meta(MasterModel.Meta):
        verbose_name = _("Contract Type")
        verbose_name_plural = _("Contract Types")


class ProjectType(MasterModel):
    class Meta(MasterModel.Meta):
        verbose_name = _("Project Type")
        verbose_name_plural = _("Project Types")


class TOP(MasterModel):
    description = models.TextField(blank=True, verbose_name=_("Description"))

    class Meta(MasterModel.Meta):
        verbose_name = _("TOP")
        verbose_name_plural = _("TOP")


class ProjectStatus(MasterModel):
    class Meta(MasterModel.Meta):
        verbose_name = _("Project Status")
        verbose_name_plural = _("Project Statuses")


class Project(TimestampedModel):
    project_code = models.CharField(
        max_length=4,
        unique=True,
        validators=[validate_business_code],
        verbose_name=_("Project Code"),
    )
    project_name = models.CharField(max_length=255, verbose_name=_("Project Name"))
    customer = models.ForeignKey(
        Customer,
        on_delete=models.PROTECT,
        related_name="projects",
        verbose_name=_("Customer"),
    )
    vendor = models.ForeignKey(
        Vendor,
        on_delete=models.PROTECT,
        related_name="projects",
        verbose_name=_("Vendor"),
    )
    contract_type = models.ForeignKey(
        ContractType,
        on_delete=models.PROTECT,
        related_name="projects",
        verbose_name=_("Contract Type"),
    )
    project_type = models.ForeignKey(
        ProjectType,
        on_delete=models.PROTECT,
        related_name="projects",
        verbose_name=_("Project Type"),
    )
    contract_start_date = models.DateField(verbose_name=_("Contract Start"))
    contract_end_date = models.DateField(verbose_name=_("Contract End"))
    top = models.ForeignKey(
        TOP,
        on_delete=models.PROTECT,
        related_name="projects",
        verbose_name=_("TOP"),
    )
    work_value = models.DecimalField(
        max_digits=18,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0"))],
        verbose_name=_("Work Value"),
    )
    project_status = models.ForeignKey(
        ProjectStatus,
        on_delete=models.PROTECT,
        related_name="projects",
        verbose_name=_("Status"),
    )
    status = models.CharField(
        max_length=8,
        choices=ActiveStatus.choices,
        default=ActiveStatus.ACTIVE,
        verbose_name=_("Record Status"),
    )

    class Meta:
        ordering = ["-contract_start_date", "project_code"]
        verbose_name = _("Project")
        verbose_name_plural = _("Projects")

    def __str__(self) -> str:
        return f"{self.project_code} - {self.project_name}"

    def clean(self) -> None:
        super().clean()
        if (
            self.contract_start_date
            and self.contract_end_date
            and self.contract_end_date < self.contract_start_date
        ):
            raise ValidationError(
                {"contract_end_date": _("Tanggal akhir kontrak tidak boleh lebih kecil dari tanggal awal.")}
            )

        for fk_field in ("customer", "vendor", "contract_type", "project_type", "top", "project_status"):
            related = getattr(self, fk_field, None)
            if related and related.status == ActiveStatus.INACTIVE:
                raise ValidationError(
                    {fk_field: _("Master data yang dipilih harus berstatus Active.")}
                )

    @property
    def remaining_contract_days(self) -> int | None:
        if not self.contract_end_date:
            return None
        from django.utils import timezone

        today = timezone.localdate()
        return (self.contract_end_date - today).days
