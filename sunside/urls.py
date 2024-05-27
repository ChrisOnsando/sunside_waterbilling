from django.urls import path
from .views import *

urlpatterns = [
    path('login/', login_user, name="login_user"),
    path('signup/', signup_user, name="signup_user"),
    path('logout/', logout_user, name="logout"),
    path('', index, name="Index"),
    path('category/', category, name="category"),
    path('viewcategory/', view_category, name="viewcategory"),
    path('viewcategory/<int:category_id>/', view_category_detail, name="view_category_detail"),
    path('editcategory/<str:category_id>/', edit_category, name="editcategory"),
    path('deletecategory/<str:category_id>/', delete_category, name="deletecategory"),
    path('savecategory/', save_category, name="savecategory"),
    path('client/', client, name="client"),
    path('viewclient/', view_client, name="viewclient"),
    path('viewclient/<int:client_id>/', view_client_detail, name="view_client_detail"),
    path('editclient/<str:client_id>/', edit_client, name="editclient"),
    path('deleteclient/<int:client_id>/', delete_client, name="deleteclient"),
    path('saveclient', save_client, name="saveclient"),
]
