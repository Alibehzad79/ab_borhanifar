from django.db import models
from django.utils.translation import gettext_lazy as _


# Create your models here.


class SiteSetting(models.Model):
    owner_name = models.CharField(max_length=100, verbose_name=_("نام مالک سایت"), blank=True, null=True)
    owner_description = models.TextField(verbose_name=_("درباره مالک سایت"), blank=True, null=True)
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


class QuestionPrice(models.Model):
    price = models.BigIntegerField(default=0, verbose_name=_("قیمت(تومان)"))

    def __str__(self):
        return str(self.price)

    class Meta:
        verbose_name = _("قیمت هر مسئله")
        verbose_name_plural = verbose_name
