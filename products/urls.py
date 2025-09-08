from django.urls import path
from . import views
from .views import create_payment

urlpatterns = [
    #api endpoints
    path('list/', views.product_list, name='product_list'),
    path('add/', views.add_products, name='add_products'),
    path('cart/add/', views.add_to_cart, name='add_to_cart'),
    path('buy-products/', views.buy_products, name='buy_products'),
    path('payment/process/', views.process_payment, name='process_payment'),
    path("payment/create_payment/", create_payment, name="create_payment"),
    path("payment/payment_notify", views.payment_notify,  name="payment_notify"),
    path('view_products/<int:pk>/', views.product_detail, name='product-detail'),

    path("cart_items/", views.get_user_cart, name="get_user_cart"),
    path("cart/update_item_count/<int:product_id>/", views.update_cart_item, name=" update_cart_item"),
    path("cart/remove_cart_item/<int:product_id>/", views.remove_cart_item, name="remove_cart_item"),
    
]
