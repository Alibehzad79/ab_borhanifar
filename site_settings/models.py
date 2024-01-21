from django.db import models
from django.utils.translation import gettext_lazy as _
from ckeditor.fields import RichTextField


# Create your models here.


class SiteSetting(models.Model):
    owner_name = models.CharField(max_length=100, verbose_name=_("نام مالک سایت"), blank=True, null=True)
    owner_description = models.TextField(verbose_name=_("درباره مالک سایت"), blank=True, null=True)
    owner_img = models.ImageField(upload_to="images/owner_img/", verbose_name=_("تصویر مالک سایت"), blank=True,
                                  null=True)
    site_name = models.CharField(max_length=100, verbose_name=_("عنوان سایت"))
    site_url = models.URLField(help_text=_("مثال: https://google.com/"))
    phone = models.CharField(max_length=100, verbose_name=_("شماره تماس"), blank=True, null=True)
    email = models.EmailField(verbose_name=_("ایمیل"), blank=True, null=True)
    site_logo = models.ImageField(upload_to="images/logos/", verbose_name=_("لوگوی سایت"), blank=True, null=True)

    def __str__(self):
        return self.site_name

    class Meta:
        verbose_name = _("تنظیم")
        verbose_name_plural = _("تنظیمات سایت")
        ordering = ["-id"]


class Seo(models.Model):
    keywords = models.TextField(verbose_name=_("کلمات کلیدی"))
    descriptions = models.TextField(verbose_name=_("توضیحات درباره سایت"))

    def __str__(self):
        return "سئو"

    class Meta:
        verbose_name = _("سئو")
        verbose_name_plural = _("سئو سایت")


class AboutMe(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("نام و نام خانوادگی"))
    description = RichTextField(verbose_name=_("درباره من"))
    phone = models.CharField(max_length=100, verbose_name=_("شماره تماس"))
    email = models.EmailField(verbose_name=_("ایمیل"))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("درباره من")
        verbose_name_plural = verbose_name


class SocialNetwork(models.Model):
    about = models.ForeignKey(AboutMe, on_delete=models.CASCADE, verbose_name=_("مدل درباره من"), related_name="socials")
    name = models.CharField(max_length=100, verbose_name=_("نام شبکه اجتماعی"), help_text=_("مثال: instagram"),
                            blank=True, null=True)
    url = models.URLField(verbose_name=_("لینک"), help_text=_("مثال: https://instagram.com/username/"), blank=True,
                          null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("شبکه")
        verbose_name_plural = _("شبکه ها")
