from django.shortcuts import render
from django.utils import timezone

from products.models import Product
from questions.models import QuestionComplete
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
        if request.user.is_superuser:
            questions = QuestionComplete.objects.filter(is_answered=False).count()
        else:
            questions = 0
        order_count = request.user.orders.filter(is_pay=False).count()
        user_question_count = request.user.questions.filter(is_pay=False).count()
    else:
        order_count = 0
        user_question_count = 0
        questions = 0
    admin_path = "/admin/questions/questioncomplete/?is_answered__exact=0"
    admin_panel = "/admin/"
    site_settings = SiteSetting.objects.last()
    context = {
        "orders_count": order_count,
        'user_question_count': user_question_count,
        "questions": questions,
        "admin_path": admin_path,
        "setting": site_settings,
        "admin_panel": admin_panel,
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
