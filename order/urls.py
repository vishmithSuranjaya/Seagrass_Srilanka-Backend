from django.urls import path
from . import views

urlpatterns = [
    path("my-orders/", views.get_orders, name="user-orders"),

    path("admin/list/", views.admin_list_orders, name="admin-orders-list"),
    path("admin/<str:order_id>/update/", views.admin_update_order_status, name="admin-orders-update"),
]