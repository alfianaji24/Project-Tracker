import re

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


BUSINESS_CODE_PATTERN = re.compile(r"^[A-Z]{4}$")


def validate_business_code(value: str) -> None:
    """Validate 4-character uppercase business code (BR-001 to BR-003)."""
    if not BUSINESS_CODE_PATTERN.match(value):
        raise ValidationError(
            _("Kode harus terdiri dari 4 huruf kapital, contoh: AWBS."),
            code="invalid_business_code",
        )
