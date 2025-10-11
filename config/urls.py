from django.contrib import admin
from django.urls import include, path
from django.views.generic.base import RedirectView

from apps.admin_users.views import (AllAdminRequestsView,
                                    CreateAdminRequestGlobalView)
from apps.root_users.views import RootLoginView


try:
    from rest_framework_simplejwt.views import \
        TokenRefreshView as _token_refresh_view
except Exception:
    _token_refresh_view = None

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
    # JWT token endpoints (RootUser-based)
    
path('api/security/', include('security.urls')),

]

if _token_refresh_view:
    urlpatterns += [
        path("api/token/refresh/", _token_refresh_view.as_view(), name="token_refresh"),
    ]
 
