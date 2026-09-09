from django.contrib.auth import views as auth_views
from django.urls import path

from core import views

urlpatterns = [
    path("login/", auth_views.LoginView.as_view(template_name="registration/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("", views.ProjectListView.as_view(), name="project_list"),
    path("dashboard/", views.DashboardView.as_view(), name="dashboard"),
    path("projects/create/", views.ProjectCreateView.as_view(), name="project_create"),
    path("projects/<int:pk>/", views.ProjectDetailView.as_view(), name="project_detail"),
    path("projects/<int:pk>/edit/", views.ProjectUpdateView.as_view(), name="project_edit"),
    path("projects/<int:pk>/deactivate/", views.project_deactivate, name="project_deactivate"),
    path("projects/<int:pk>/reactivate/", views.project_reactivate, name="project_reactivate"),
]
