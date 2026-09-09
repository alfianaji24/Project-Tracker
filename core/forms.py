from django import forms
from django.utils.translation import gettext_lazy as _

from core.models import (
    ActiveStatus,
    ContractType,
    Customer,
    Project,
    ProjectStatus,
    ProjectType,
    TOP,
    Vendor,
)


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = [
            "project_code",
            "project_name",
            "customer",
            "vendor",
            "contract_type",
            "project_type",
            "contract_start_date",
            "contract_end_date",
            "top",
            "work_value",
            "project_status",
        ]
        widgets = {
            "project_code": forms.TextInput(
                attrs={"class": "form-control", "maxlength": "4", "style": "text-transform: uppercase;"}
            ),
            "project_name": forms.TextInput(attrs={"class": "form-control"}),
            "customer": forms.Select(attrs={"class": "form-select"}),
            "vendor": forms.Select(attrs={"class": "form-select"}),
            "contract_type": forms.Select(attrs={"class": "form-select"}),
            "project_type": forms.Select(attrs={"class": "form-select"}),
            "contract_start_date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "contract_end_date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "top": forms.Select(attrs={"class": "form-select"}),
            "work_value": forms.NumberInput(attrs={"class": "form-control", "step": "0.01", "min": "0"}),
            "project_status": forms.Select(attrs={"class": "form-select"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["customer"].queryset = Customer.objects.filter(status=ActiveStatus.ACTIVE)
        self.fields["vendor"].queryset = Vendor.objects.filter(status=ActiveStatus.ACTIVE)
        self.fields["contract_type"].queryset = ContractType.objects.filter(status=ActiveStatus.ACTIVE)
        self.fields["project_type"].queryset = ProjectType.objects.filter(status=ActiveStatus.ACTIVE)
        self.fields["top"].queryset = TOP.objects.filter(status=ActiveStatus.ACTIVE)
        self.fields["project_status"].queryset = ProjectStatus.objects.filter(status=ActiveStatus.ACTIVE)

    def clean_project_code(self):
        code = self.cleaned_data["project_code"].upper().strip()
        qs = Project.objects.filter(project_code=code)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError(_("Project code sudah digunakan."))
        return code


class ProjectFilterForm(forms.Form):
    q = forms.CharField(
        required=False,
        label=_("Cari"),
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Project code atau nama..."}
        ),
    )
    customer = forms.ModelChoiceField(
        queryset=Customer.objects.filter(status=ActiveStatus.ACTIVE),
        required=False,
        empty_label=_("Semua Customer"),
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    vendor = forms.ModelChoiceField(
        queryset=Vendor.objects.filter(status=ActiveStatus.ACTIVE),
        required=False,
        empty_label=_("Semua Vendor"),
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    contract_type = forms.ModelChoiceField(
        queryset=ContractType.objects.filter(status=ActiveStatus.ACTIVE),
        required=False,
        empty_label=_("Semua Kontrak"),
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    project_type = forms.ModelChoiceField(
        queryset=ProjectType.objects.filter(status=ActiveStatus.ACTIVE),
        required=False,
        empty_label=_("Semua Tipe"),
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    top = forms.ModelChoiceField(
        queryset=TOP.objects.filter(status=ActiveStatus.ACTIVE),
        required=False,
        empty_label=_("Semua TOP"),
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    project_status = forms.ModelChoiceField(
        queryset=ProjectStatus.objects.filter(status=ActiveStatus.ACTIVE),
        required=False,
        empty_label=_("Semua Status"),
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    contract_start_from = forms.DateField(
        required=False,
        label=_("Kontrak Mulai Dari"),
        widget=forms.DateInput(attrs={"class": "form-control", "type": "date"}),
    )
    contract_start_to = forms.DateField(
        required=False,
        label=_("Kontrak Mulai Sampai"),
        widget=forms.DateInput(attrs={"class": "form-control", "type": "date"}),
    )
    contract_end_from = forms.DateField(
        required=False,
        label=_("Kontrak Selesai Dari"),
        widget=forms.DateInput(attrs={"class": "form-control", "type": "date"}),
    )
    contract_end_to = forms.DateField(
        required=False,
        label=_("Kontrak Selesai Sampai"),
        widget=forms.DateInput(attrs={"class": "form-control", "type": "date"}),
    )
    show_inactive = forms.BooleanField(
        required=False,
        label=_("Tampilkan project nonaktif"),
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
    )
