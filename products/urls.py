from django.urls import path
from . import views
from .views import create_payment

urlpatterns = [
    #api endpoints
    path('list/', views.product_list, name='product_list'),
    path('cart/add/', views.add_to_cart, name='add_to_cart'),
    path('buy-products/', views.buy_products, name='buy_products'),
    path('payment/process/', views.process_payment, name='process_payment'),
    path("payment/create_payment/", create_payment, name="create_payment"),
    path("payment/payment_notify", views.payment_notify,  name="payment_notify"),
    path('view_products/<str:product_id>/', views.product_detail, name='product-detail'),
    path('payment/save_payment/', views.save_payment, name="save_payment"),

    # Admin-only endpoints
    path('admin/list/', views.admin_product_list, name='admin_product_list'),
    
    path('admin/add/', views.add_products, name='add_products'),
    path('admin/<str:product_id>/update/', views.update_product, name='update_product'),
    path('admin/<str:product_id>/delete/', views.delete_product, name='delete_product'),

    path("cart_items/", views.get_user_cart, name="get_user_cart"),
    path("cart/update_item_count/<str:product_id>/", views.update_cart_item, name=" update_cart_item"),
    path("cart/remove_cart_item/<str:product_id>/", views.remove_cart_item, name="remove_cart_item"),
    
]
