from django.urls import path

from .views import CreateAdminView, LoginView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('create-admin/', CreateAdminView.as_view(), name='create-admin'),
]
