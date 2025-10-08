from django.urls import path

from .views import (CreateRootUserView, DeleteRootUserView, RootLoginView,
                    UpdateRootPasswordView)

urlpatterns = [
    path("createrootuser/", CreateRootUserView.as_view(), name="create-root-user"),
    path("<int:root_id>/updaterootpassword/", UpdateRootPasswordView.as_view(), name="update-root-password"),
    path("<int:root_id>/deleterootuser/", DeleteRootUserView.as_view(), name="delete-root-user"),
    path("login/", RootLoginView.as_view(), name="root-login"),

]
