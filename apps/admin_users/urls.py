from django.urls import path

from .views import (
    CreateAdminRequestView,
    ListAdminRequestsView,
    CreateAdminAccountView,
    RejectAdminRequestView,
    UpdateRootUserPasswordView,
    DeleteRootUserView,
)

urlpatterns = [
    path("create-admin-request/", CreateAdminRequestView.as_view(), name="create-admin-request"),
    path("admin-requests/", ListAdminRequestsView.as_view(), name="list-admin-requests"),
    path("createadminaccount/<int:request_id>/", CreateAdminAccountView.as_view(), name="create-admin-account"),
    path("reject-admin-request/<int:request_id>/", RejectAdminRequestView.as_view(), name="reject-admin-request"),
    path("update-password/", UpdateRootUserPasswordView.as_view(), name="update-root-password"),
    path("delete/", DeleteRootUserView.as_view(), name="delete-root-user"),
]
