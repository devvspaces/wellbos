from django.urls import path

from . import views


app_name='product'
urlpatterns = [
    path('<str:category>/', views.CategorySubList.as_view(), name='category'),
    path('<str:category>/<str:sub>/', views.ProductList.as_view(), name='product-list'),
    path('<str:category>/<str:sub>/<str:code>/', views.ProductDetail.as_view(), name='product-detail'),
]
