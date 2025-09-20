from django.urls import path
from . import views

urlpatterns = [
    path("my-orders/", views.get_orders, name="user-orders"),
]