from azbankgateways.exceptions import AZBankGatewaysException
from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages
from orders.models import Order, CompleteOrder
from products.models import Product

from azbankgateways.exceptions import AZBankGatewaysException
from django.urls import reverse
from azbankgateways import bankfactories, models as bank_models, default_settings as settings


@login_required(login_url="login")
def go_to_gateway_view(request):
    user = request.user
    orders = user.orders.filter(is_pay=False).all()
    print(orders)
    user_amount = 0
    for order in orders:
        user_amount += order.price

    amount = user_amount * 10
    factory = bankfactories.BankFactory()
    try:
        bank = factory.auto_create()  # or factory.create(bank_models.BankType.BMI) or set identifier
        bank.set_request(request)
        bank.set_amount(amount)
        # یو آر ال بازگشت به نرم افزار برای ادامه فرآیند
        bank.set_client_callback_url(reverse('order:callback-gateway'))

        # در صورت تمایل اتصال این رکورد به رکورد فاکتور یا هر چیزی که بعدا بتوانید ارتباط بین محصول یا خدمات را با این
        # پرداخت برقرار کنید.
        bank_record = bank.ready()

        # هدایت کاربر به درگاه بانک
        context = bank.get_gateway()
        return render(request, 'order/redirect_to_bank.html', context=context)
        # return bank.redirect_gateway()
    except AZBankGatewaysException as e:
        return render(request, 'order/redirect_to_bank.html')


@login_required(login_url="login")
def callback_gateway_view(request):
    tracking_code = request.GET.get(settings.TRACKING_CODE_QUERY_PARAM, None)
    if not tracking_code:
        messages.add_message(request, message="پرداخت موفقیت آمیز نبود", level=messages.ERROR)
        return redirect("home_page")

    try:
        bank_record = bank_models.Bank.objects.get(tracking_code=tracking_code)
    except bank_models.Bank.DoesNotExist:
        messages.add_message(request, message="پرداخت موفقیت آمیز نبود", level=messages.ERROR)
        return redirect("home_page")

    # در این قسمت باید از طریق داده هایی که در بانک رکورد وجود دارد، رکورد متناظر یا هر اقدام مقتضی دیگر را انجام دهیم
    if bank_record.is_success:
        user = request.user
        orders = user.orders.filter(is_pay=False).all()
        for order in orders:
            new_comp_order = CompleteOrder.objects.create(user=user, product=order.product, price=order.price,
                                                          date_created=timezone.now())
            if new_comp_order is not None:
                new_comp_order.save()
                order.is_pay = True
                order.save()
        messages.add_message(request, message="پرداخت موفقیت آمیز بود", level=messages.SUCCESS)
        return redirect("downloads")
    # پرداخت موفق نبوده است. اگر پول کم شده است ظرف مدت ۴۸ ساعت پول به حساب شما بازخواهد گشت.
    messages.add_message(request,
                         message="پرداخت با شکست مواجه شده است. اگر پول کم شده است ظرف مدت ۴۸ ساعت پول به حساب شما بازخواهد گشت. ",
                         level=messages.ERROR)
    return redirect("home_page")


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
    try:
        order = user.orders.get(id=order_id)
        Order.delete(order)
        messages.add_message(request, message="با موفقت حذف شد.", level=messages.ERROR)
        return redirect('order:orders')
    except:
        raise Http404
