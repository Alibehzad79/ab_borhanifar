from django.shortcuts import render
from django.utils import timezone

from products.models import Product
from site_settings.models import SiteSetting, Seo, AboutMe


def home_page(request):
    template_name = "index.html"
    products = Product.objects.all()
    seo = Seo.objects.last()
    site_settings = SiteSetting.objects.last()
    context = {
        "products": products,
        'seo': seo,
        "settings": site_settings,
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

    site_settings = SiteSetting.objects.last()
    three_last_products = Product.objects.all()[:3]
    date = timezone.now().year
    context = {
        "settings": site_settings,
        'products': three_last_products,
        "date": date,
    }
    return render(request, template_name, context)


def about_me(request):
    template_name = "about_me.html"
    about = AboutMe.objects.last()
    context = {
        "about": about,
    }
    return render(request, template_name, context)
