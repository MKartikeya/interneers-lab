from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.ProductView.as_view(), name='product_list'),
    path('products/<int:product_id>/', views.ProductView.as_view(), name='product_detail'),
    path('categories/', views.CategoryView.as_view(), name='category_list'),
    path('categories/<int:category_id>/', views.CategoryView.as_view(), name='category_detail'),
    path('brands/', views.BrandView.as_view(), name='brand_list'),
    path('brands/<int:brand_id>/', views.BrandView.as_view(), name='brand_detail'),
    path('inventories/', views.InventoryView.as_view(), name='inventory_list'),
    path('inventories/<int:inventory_id>/', views.InventoryView.as_view(), name='inventory_detail'),
]