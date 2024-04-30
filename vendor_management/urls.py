"""
URL configuration for vendor_management project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path


from django.urls import path
from app import views


urlpatterns = [
    path('api/vendors/', views.VendorListCreateAPIView.as_view(), name='vendor_list_create'),
    path('api/vendors/<int:pk>/', views.VendorRetrieveUpdateDestroyAPIView.as_view(), name='vendor_retrieve_update_destroy'),
    path('api/purchase_orders/', views.PurchaseOrderListCreateAPIView.as_view(), name='purchase_order_list_create'),
    path('api/purchase_orders/<int:pk>/', views.PurchaseOrderRetrieveUpdateDestroyAPIView.as_view(), name='purchase_order_retrieve_update_destroy'),
    path('api/vendors/<int:pk>/performance/', views.VendorPerformanceAPIView.as_view(), name='vendor_performance'),
]
