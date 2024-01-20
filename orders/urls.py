from django.urls import path
from orders.views import add_order, orders, remove_order

urlpatterns = [
    path('add-order/product/<int:pk>/', add_order, name="add_order"),
    path('user-orders/', orders, name="orders"),
    path('remove/<int:pk>/', remove_order, name="remove_order"),
]
