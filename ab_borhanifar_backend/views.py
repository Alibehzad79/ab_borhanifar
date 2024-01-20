from django.shortcuts import render

from products.models import Product


def home_page(request):
    template_name = "index.html"
    products = Product.objects.all()
    context = {
        "products": products,
    }
    return render(request, template_name, context)


def header(request):
    template_name = "base/header.html"
    if request.user.is_authenticated:
        order_count = request.user.orders.filter(is_pay=False).count()
    else:
        order_count = 0
    context = {
        "orders_count": order_count,
    }
    return render(request, template_name, context)


def footer(request):
    template_name = "base/footer.html"
    context = {}
    return render(request, template_name, context)
