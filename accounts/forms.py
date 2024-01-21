from django import forms
from django.contrib.auth import get_user_model


class LoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "example@mail.com"}))

    password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control"}))

    remember_me = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={"class": "form-check-input", "checked": "true"}, ))

    def clean_email(self):
        email = self.cleaned_data.get("email")
        email_exists = get_user_model().objects.filter(email=email).exists()
        if not email_exists:
            raise forms.ValidationError("کاربری با این ایمیل یافت نشده")
        return email


class RegisterForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "username"}),
                               max_length=20)
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "example@mail.com"}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control"}), min_length=6,
                                max_length=12)
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control"}), min_length=6,
                                max_length=12)

    def clean_username(self):
        username = self.cleaned_data.get("username")
        username_exists = get_user_model().objects.filter(username=username).exists()
        if username_exists:
            raise forms.ValidationError("کاربری با این نام کاربری قبلا ثبت نام کرده است.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get("email")
        email_exists = get_user_model().objects.filter(email=email).exists()
        if email_exists:
            raise forms.ValidationError("کاربری قبلا با این ایمیل ثبت نام کرده است.")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 != password2:
            raise forms.ValidationError("رمز عبور ها یکسان نیستند.")
        return password1


class ProfileForm(forms.Form):
    first_name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}), max_length=50)
    last_name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}), max_length=50)


class ChangePasswordForm(forms.Form):
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control"}), min_length=6,
                                max_length=12)
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control"}), min_length=6,
                                max_length=12)

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 != password2:
            raise forms.ValidationError("رمز عبور ها یکسان نیستند.")
        return password1
