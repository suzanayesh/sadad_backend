from django.urls import path
from .views import Root_User_List, Root_User_Create, Root_User_Update, Root_User_Delete

urlpatterns = [
    path('', Root_User_List, name='Root_User_List'),
    path('create/', Root_User_Create, name='Root_User_Create'),
    path('update/<int:pk>/', Root_User_Update, name='Root_User_Update'),
    path('delete/<int:pk>/', Root_User_Delete, name='Root_User_Delete'),
]