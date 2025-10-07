from django.contrib import admin
from django.urls import include, path
from django.views.generic.base import RedirectView

from apps.admin_users.views import CreateAdminRequestGlobalView
from apps.admin_users.views import AllAdminRequestsView
from apps.root_users.views import RootLoginView

urlpatterns = [
    # Redirect root '/' to the API base
    path("", RedirectView.as_view(url='/api/', permanent=False)),
    path("admin/", admin.site.urls),
    path("api/", include("apps.root_users.urls")),
    path("api/root/<int:root_id>/", include("apps.admin_users.urls")),
    path("api/create-admin-request/", CreateAdminRequestGlobalView.as_view(), name="create-admin-request-global"),
    path("api/admin/request/", CreateAdminRequestGlobalView.as_view(), name="create-admin-request"),
    path("api/admin-requests/", AllAdminRequestsView.as_view(), name="all-admin-requests"),
    # alias so POST /api/root/login/ (used by the client) works
    path("api/root/login/", RootLoginView.as_view(), name="root-login-alias"),
]
