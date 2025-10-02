from django.urls import path
from .views import (
    Root_User_List, Root_User_Create, Root_User_Update, Root_User_Delete,
    root_user_api, root_user_detail_api
)

urlpatterns = [
    path('', Root_User_List, name='Root_User_List'),
    path('create/', Root_User_Create, name='Root_User_Create'),
    path('update/<int:pk>/', Root_User_Update, name='Root_User_Update'),
    path('delete/<int:pk>/', Root_User_Delete, name='Root_User_Delete'),
    # API endpoints
    path('api/', root_user_api, name='root_user_api'),
    path('api/<int:pk>/', root_user_detail_api, name='root_user_detail_api'),
]