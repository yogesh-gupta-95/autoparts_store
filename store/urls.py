from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('cart/', views.cart_view, name='cart'),
    path('add-to-cart/<int:pk>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:pk>/', views.remove_from_cart, name='remove_from_cart'),
    path('update-cart/<int:pk>/', views.update_cart, name='update_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('payment/', views.payment, name='payment'),
    path('order-success/', views.order_success, name='order_success'),
    path('orders/', views.order_history, name='order_history'),
    path('order-tracking/<int:pk>/', views.order_tracking, name='order_tracking'),
    path('search/', views.search, name='search'),
    path('browse-by-car/', views.browse_by_car, name='browse_by_car'),
    path('sales-report/', views.sales_report, name='sales_report'),
]