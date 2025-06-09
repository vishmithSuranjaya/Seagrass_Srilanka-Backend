from django.urls import path
from . import views

urlpatterns = [
    #api endpoints
    path('products/list/', views.product_list, name='product_list'),
    path('products/add/', views.add_products, name='add_products'),
    path('cart/add/', views.add_to_cart, name='add_to_cart'),
    path('buy-products/', views.buy_products, name='buy_products'),
    path('payment/process/', views.process_payment, name='process_payment'),
]