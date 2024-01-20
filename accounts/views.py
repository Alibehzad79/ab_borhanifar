from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout, get_user_model
from accounts.forms import LoginForm, RegisterForm
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
