from django.contrib import admin
from django.urls import include, path

admin.site.site_header = "Project & Contract Management"
admin.site.site_title = "Project Tracker"
admin.site.index_title = "Dashboard Admin"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("core.urls")),
]
