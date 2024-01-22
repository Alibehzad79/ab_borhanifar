from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.core.mail import send_mail
from accounts.forms import LoginForm, RegisterForm, ProfileForm, ChangePasswordForm, RecoveryPasswordForm
from django.contrib.auth.hashers import make_password, get_random_string
from django.contrib import messages
from ab_borhanifar_backend.settings import DEFAULT_FROM_EMAIL
from azbankgateways.exceptions import AZBankGatewaysException
from django.urls import reverse
from azbankgateways import bankfactories, models as bank_models, default_settings as settings

from questions.models import QuestionComplete, Question
from site_settings.models import SiteSetting


# Create your views here.

def login_page(request):
    template_name = 'accounts/login.html'
    if request.user.is_authenticated:
        return redirect("home_page")
    if request.method == "POST":
        form = LoginForm(request.POST or None)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            remember_me = form.cleaned_data.get("remember_me")
            username = get_user_model().objects.get(email=email).username
            get_user = get_user_model().objects.get(username=username)
            user = authenticate(request, username=get_user.username, password=password)
            if user is not None:
                login(request, user)
                if not remember_me:
                    request.session.set_expiry(0)
                messages.add_message(request, message="با موفقیت وارد شدید", level=messages.SUCCESS)
                return redirect('home_page')
            else:
                form.add_error('password', "ایمیل یا رمز عبور اشتباه است.")
    else:
        form = LoginForm()
    context = {
        'form': form,
    }
    return render(request, template_name, context)


def register_page(request):
    template_name = "accounts/register.html"
    if request.user.is_authenticated:
        return redirect("home_page")
    if request.method == "POST":
        form = RegisterForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password1")
            password_encrypt = make_password(password)
            new_user = get_user_model().objects.create(username=username, email=email, password=password_encrypt)
            if new_user is not None:
                new_user.save()
                messages.add_message(request, message="با موفقیت ثبت نام شدید.", level=messages.SUCCESS)
                return redirect("login")
            else:
                form.add_error('password2', 'کاربری قبلا با مشخصات وارد شده، ثبت نام کرده است.')
    else:
        form = RegisterForm()

    context = {
        "form": form,
    }
    return render(request, template_name, context)


def logout_page(request):
    logout(request)
    return redirect("login")


@login_required(login_url="login")
def sidebar(request):
    if not request.user.is_authenticated:
        return redirect("login")

    template_name = "accounts/sidebar.html"
    context = {

    }
    return render(request, template_name, context)


@login_required(login_url="login")
def question_sidebar(request):
    if not request.user.is_authenticated:
        return redirect("login")

    template_name = "accounts/user_question_sidebar.html"
    context = {

    }
    return render(request, template_name, context)


@login_required(login_url="login")
def profile(request):
    if not request.user.is_authenticated:
        return redirect("login")

    template_name = "accounts/profile.html"

    if request.method == 'POST':
        form = ProfileForm(request.POST or None)
        if form.is_valid():
            user = request.user
            first_name = form.cleaned_data.get("first_name")
            last_name = form.cleaned_data.get("last_name")
            user.first_name = first_name
            user.last_name = last_name
            user.save()
            messages.add_message(request, message="با موفقیت تغییر یافت.", level=messages.SUCCESS)
            return redirect("profile")
    else:
        form = ProfileForm(initial={"first_name": request.user.first_name, "last_name": request.user.last_name})

    context = {
        "user": request.user,
        'form': form,
    }
    return render(request, template_name, context)


@login_required(login_url="login")
def change_password(request):
    if not request.user.is_authenticated:
        return redirect("login")
    template_name = "accounts/change_password.html"
    if request.method == "POST":
        form = ChangePasswordForm(request.POST or None)
        if form.is_valid():
            password1 = form.cleaned_data.get("password1")
            user = request.user
            user.set_password(password1)
            user.save()
            messages.add_message(request, message="رمز عبور با موفقیت تغییر یافت", level=messages.SUCCESS)
            return redirect("change_password")
    else:
        form = ChangePasswordForm()

    context = {"form": form, }
    return render(request, template_name, context)


def recovery_password(request):
    template_name = 'accounts/recovery_password.html'
    if request.user.is_authenticated:
        return redirect("home_page")
    if request.method == "POST":
        form = RecoveryPasswordForm(request.POST or None)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            user = get_user_model().objects.get(email=email)
            rec_hash = get_random_string(32)
            user.user_password_rest_token = rec_hash
            user.save()
            site_settings = SiteSetting.objects.last()
            a_href = f'<a href="{site_settings.site_url}accounts/recovery-password/set-password/?key={rec_hash}' + '</a>'
            send_mail(subject="بازیابی رمز عبور", message=f"{a_href}برای یازیابی رمز عبور، کلیک کنید \n ",
                      from_email=DEFAULT_FROM_EMAIL, recipient_list=[email], fail_silently=False)
            return redirect("send_email_done")
    else:
        form = RecoveryPasswordForm()
    context = {
        "form": form,
    }
    return render(request, template_name, context)


def send_email_done(request):
    template_name = 'accounts/send_email_done.html'
    context = {}
    return render(request, template_name, context)


def set_recovery_password(request, **kwargs):
    template_name = "accounts/set_recovery_password.html"
    rec_hash = request.GET.get("key")
    print(rec_hash)
    try:
        user = get_user_model().objects.get(user_password_rest_token=rec_hash)
        print(user)
    except:
        user = None
    if user is None:
        messages.add_message(request, message="توکن نامعتبر است", level=messages.ERROR)
        return redirect("home_page")

    if rec_hash != user.user_password_rest_token:
        messages.add_message(request, message="توکن نامعتبر است", level=messages.ERROR)
        return redirect("home_page")

    if request.method == "POST":
        form = ChangePasswordForm(request.POST or None)
        if form.is_valid():
            password = form.cleaned_data.get("password1")
            user.set_password(password)
            user.user_password_rest_token = None
            user.save()
            messages.add_message(request, message="رمز عبور با موفقیت تغییر یافت", level=messages.SUCCESS)
            return redirect("login")
    else:
        form = ChangePasswordForm()

    context = {
        'form': form,
        'rec_hash': rec_hash,
    }
    return render(request, template_name, context)


@login_required(login_url="login")
def user_downloads(request):
    if not request.user.is_authenticated:
        return redirect("login")
    template_name = 'accounts/downloads.html'
    user = request.user
    user_downloads = user.com_orders.all()

    context = {
        'downloads': user_downloads,
    }
    return render(request, template_name, context)


@login_required(login_url="login")
def go_to_gateway_view(request):
    user = request.user
    questions = user.questions.filter(is_pay=False).all()
    user_amount = 0
    for ques in questions:
        user_amount += int(ques.price)
    amount = user_amount * 10
    print(amount)
    factory = bankfactories.BankFactory()
    try:
        bank = factory.auto_create()  # or factory.create(bank_models.BankType.BMI) or set identifier
        bank.set_request(request)
        bank.set_amount(amount)
        # یو آر ال بازگشت به نرم افزار برای ادامه فرآیند
        bank.set_client_callback_url(reverse('question_app:callback-gateway'))

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
        questions = user.questions.filter(is_pay=False).all()
        for ques in questions:
            new_question_complete = QuestionComplete.objects.create(user=user, question=ques,
                                                                    question_title=ques.question_title,
                                                                    question_count=ques.question_count,
                                                                    question_file=ques.image,
                                                                    price=ques.price, date_created=timezone.now(),
                                                                    email=ques.email)
            if new_question_complete is not None:
                new_question_complete.save()
                ques.is_pay = True
                ques.save()
        messages.add_message(request, message="پرداخت موفقیت آمیز بود", level=messages.SUCCESS)
        return redirect("questions-complete")
    # پرداخت موفق نبوده است. اگر پول کم شده است ظرف مدت ۴۸ ساعت پول به حساب شما بازخواهد گشت.
    messages.add_message(request,
                         message="پرداخت با شکست مواجه شده است. اگر پول کم شده است ظرف مدت ۴۸ ساعت پول به حساب شما بازخواهد گشت ",
                         level=messages.ERROR)
    return redirect("home_page")


@login_required(login_url="login")
def user_questions(request):
    if not request.user.is_authenticated:
        return redirect("login")
    template_name = "accounts/user_questions.html"
    user = request.user
    questions = user.questions.filter(is_pay=False).all()
    amount = 0
    for ques in questions:
        amount += int(ques.price)
    context = {
        "questions": questions,
        'amount': amount,
    }
    return render(request, template_name, context)


@login_required(login_url="login")
def delete_question(request, **kwargs):
    question_id = kwargs["pk"]
    user = request.user
    try:
        question = Question.objects.get(id=question_id, is_pay=False)
        question.delete()
        messages.add_message(request, message="با موفقیت حذف شد.", level=messages.ERROR)
        return redirect('user_questions')
    except:
        return redirect("home_page")


@login_required(login_url="login")
def user_questions_complete(request):
    if not request.user.is_authenticated:
        return redirect("login")
    template_name = "accounts/user_question_complete.html"
    user = request.user
    questions = user.comp_question.all()
    context = {
        "questions_comp": questions,
    }
    return render(request, template_name, context)
