# core/urls.py

from django.urls import path
from . import views

urlpatterns = [
# Match the updated, more descriptive view names
    path("dashboard/", views.dashboard_view, name="dashboard"),
    path("create/", views.create_repo_view, name="create_repo"),
    path("python-env/", views.python_env_view, name="python_env"),
# Python compiler API
    path("api/run-code/", views.run_code_view, name="run_code"),
# Repository detail and basic file management
    path("<str:username>/<str:repo_name>/", views.repository_detail_view, name="repository_detail"),
    path("<str:username>/<str:repo_name>/create/", views.create_file_view, name="create_file"),
    path("<str:username>/<str:repo_name>/edit/<int:file_id>/", views.edit_file_view, name="edit_file"),
    path("<str:username>/<str:repo_name>/delete/<int:file_id>/", views.delete_file_view, name="delete_file"),
    path("<str:username>/<str:repo_name>/upload/", views.upload_file_view, name="upload_file"),
# Repository-level edit and delete (new routes)
    path("<str:username>/<str:repo_name>/settings/", views.repository_settings_view, name="repository_settings"),
    path("<str:username>/<str:repo_name>/edit-repo/", views.edit_repository_view, name="edit_repository"),
    path("<str:username>/<str:repo_name>/delete-repo/", views.delete_repository_view, name="delete_repository"),
# Download entire repository as ZIP
    path("<str:username>/<str:repo_name>/download/", views.download_repository_view, name="download_repository"),
]
