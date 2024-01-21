from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages
from orders.models import Order
from products.models import Product


# Create your views here.

@login_required(login_url="login")
def add_order(request, **kwargs):
    if not request.user.is_authenticated:
        return redirect("login")
    product_id = kwargs['pk']
    user = request.user
    try:
        product = Product.objects.get(id=product_id)
    except:
        return redirect("home_page")

    new_order = Order.objects.create(user=user, product=product, price=product.price,
                                     date_created=timezone.now())
    if new_order is not None:
        new_order.save()
        messages.add_message(request, message="با موفقت به سبد خرید اضافه شد.", level=messages.SUCCESS)
        return redirect("home_page")


@login_required(login_url="login")
def orders(request):
    template_name = "order/orders.html"
    if not request.user.is_authenticated:
        return redirect("login")
    user = request.user
    orders = user.orders.filter(is_pay=False).all()
    amount = 0
    for order in orders:
        amount += order.price
    context = {
        "orders": orders,
        "amount": amount,
    }

    return render(request, template_name, context)


@login_required(login_url="login")
def remove_order(request, **kwargs):
    order_id = kwargs['pk']
    user = request.user
    order = user.orders.get(id=order_id)
    Order.delete(order)
    messages.add_message(request, message="با موفقت حذف شد.", level=messages.ERROR)
    return redirect('orders')
