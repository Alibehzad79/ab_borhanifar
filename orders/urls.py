from django.urls import path
from orders.views import add_order, orders, remove_order, callback_gateway_view, go_to_gateway_view

app_name = "order"
urlpatterns = [
    path('add-order/product/<int:pk>/', add_order, name="add_order"),
    path('user-orders/', orders, name="orders"),
    path('remove/<int:pk>/', remove_order, name="remove_order"),
    path('callback-gateway/', callback_gateway_view, name="callback-gateway"),
    path('go-to-gateway-view/', go_to_gateway_view, name="go-to-gateway-view"),
]
