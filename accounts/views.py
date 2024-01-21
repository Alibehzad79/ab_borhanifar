from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout, get_user_model
from django.contrib.auth.decorators import login_required
from accounts.forms import LoginForm, RegisterForm, ProfileForm, ChangePasswordForm
from django.contrib.auth.hashers import make_password
from django.contrib import messages


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
            print(get_user.username, get_user.password)
            user = authenticate(request, username=get_user.username, password=password)
            if user is not None:
                login(request, user)
                if not remember_me:
                    request.session.set_expiry(0)
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
def user_questions(request):
    if not request.user.is_authenticated:
        return redirect("login")
    template_name = "accounts/user_questions.html"
    user = request.user
    questions = user.questions.all()

    context = {
        "questions": questions,
    }
    return render(request, template_name, context)
