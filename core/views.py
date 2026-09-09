from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, Count
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DetailView, ListView, UpdateView, TemplateView
from django.utils import timezone
from datetime import timedelta

from core.forms import ProjectFilterForm, ProjectForm
from core.models import ActiveStatus, Project


class ProjectListView(LoginRequiredMixin, ListView):
    model = Project
    template_name = "core/project_list.html"
    context_object_name = "projects"
    paginate_by = 15

    def get_queryset(self):
        queryset = (
            Project.objects.select_related(
                "customer",
                "vendor",
                "contract_type",
                "project_type",
                "top",
                "project_status",
            )
            .order_by("-contract_start_date", "project_code")
        )

        self.filter_form = ProjectFilterForm(self.request.GET or None)
        if not self.filter_form.is_valid():
            return queryset.filter(status=ActiveStatus.ACTIVE)

        data = self.filter_form.cleaned_data
        if not data.get("show_inactive"):
            queryset = queryset.filter(status=ActiveStatus.ACTIVE)

        if data.get("q"):
            term = data["q"].strip()
            queryset = queryset.filter(
                Q(project_code__icontains=term) | Q(project_name__icontains=term)
            )
        if data.get("customer"):
            queryset = queryset.filter(customer=data["customer"])
        if data.get("vendor"):
            queryset = queryset.filter(vendor=data["vendor"])
        if data.get("contract_type"):
            queryset = queryset.filter(contract_type=data["contract_type"])
        if data.get("project_type"):
            queryset = queryset.filter(project_type=data["project_type"])
        if data.get("top"):
            queryset = queryset.filter(top=data["top"])
        if data.get("project_status"):
            queryset = queryset.filter(project_status=data["project_status"])
        if data.get("contract_start_from"):
            queryset = queryset.filter(contract_start_date__gte=data["contract_start_from"])
        if data.get("contract_start_to"):
            queryset = queryset.filter(contract_start_date__lte=data["contract_start_to"])
        if data.get("contract_end_from"):
            queryset = queryset.filter(contract_end_date__gte=data["contract_end_from"])
        if data.get("contract_end_to"):
            queryset = queryset.filter(contract_end_date__lte=data["contract_end_to"])

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filter_form"] = getattr(self, "filter_form", ProjectFilterForm())
        context["total_count"] = context["paginator"].count
        return context


class ProjectDetailView(LoginRequiredMixin, DetailView):
    model = Project
    template_name = "core/project_detail.html"
    context_object_name = "project"

    def get_queryset(self):
        return Project.objects.select_related(
            "customer",
            "vendor",
            "contract_type",
            "project_type",
            "top",
            "project_status",
        )


class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    form_class = ProjectForm
    template_name = "core/project_form.html"
    success_url = reverse_lazy("project_list")

    def form_valid(self, form):
        messages.success(self.request, _("Project berhasil dibuat."))
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = _("Tambah Project")
        context["submit_label"] = _("Simpan Project")
        return context


class ProjectUpdateView(LoginRequiredMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = "core/project_form.html"

    def get_success_url(self):
        return reverse_lazy("project_detail", kwargs={"pk": self.object.pk})

    def form_valid(self, form):
        messages.success(self.request, _("Project berhasil diperbarui."))
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = _("Edit Project")
        context["submit_label"] = _("Perbarui Project")
        return context


@login_required
def project_deactivate(request, pk):
    project = get_object_or_404(Project, pk=pk)

    if request.method == "POST":
        project.status = ActiveStatus.INACTIVE
        project.save(update_fields=["status", "updated_at"])
        messages.success(request, _("Project '%(name)s' telah dinonaktifkan.") % {"name": project.project_name})
        return redirect("project_list")

    return render(request, "core/project_confirm_deactivate.html", {"project": project})


@login_required
def project_reactivate(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == "POST":
        project.status = ActiveStatus.ACTIVE
        project.save(update_fields=["status", "updated_at"])
        messages.success(request, _("Project '%(name)s' telah diaktifkan kembali.") % {"name": project.project_name})
        return redirect("project_detail", pk=project.pk)
    return redirect("project_detail", pk=project.pk)


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "core/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = timezone.localdate()
        context["total_count"] = Project.objects.count()
        context["by_status"] = (
            Project.objects.values("project_status__code", "project_status__name")
            .annotate(count=Count("id"))
            .order_by("-count")
        )
        context["by_type"] = (
            Project.objects.values("project_type__code", "project_type__name")
            .annotate(count=Count("id"))
            .order_by("-count")
        )
        context["by_customer"] = (
            Project.objects.values("customer__code", "customer__name")
            .annotate(count=Count("id"))
            .order_by("-count")[:20]
        )
        context["expiring_soon"] = Project.objects.filter(
            contract_end_date__gte=today, contract_end_date__lte=today + timedelta(days=30)
        ).order_by("contract_end_date")[:20]
        context["expired"] = Project.objects.filter(
            contract_end_date__lt=today
        ).order_by("-contract_end_date")[:20]
        context["expiring_soon_count"] = Project.objects.filter(
            contract_end_date__gte=today, contract_end_date__lte=today + timedelta(days=30)
        ).count()
        context["expired_count"] = Project.objects.filter(contract_end_date__lt=today).count()
        return context
