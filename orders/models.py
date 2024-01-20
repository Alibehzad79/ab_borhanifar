from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

from products.models import Product


# Create your models here.

class Order(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.DO_NOTHING, related_name="orders",
                             verbose_name=_("کاربر"))
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING, verbose_name=_("محصول"))
    price = models.BigIntegerField(default=0, verbose_name=_("قیمت کل"))
    is_pay = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now=False, auto_now_add=False, verbose_name=_("تاریخ ایجاد"))

    def get_amount(self):
        amount = 0
        for order in self.objects.all():
            amount += order.price

        return amount

    def __str__(self):
        return self.user.username + f" #{self.id} "

    class Meta:
        verbose_name = _("سبد خرید")
        verbose_name_plural = _("سبد خرید کاربران")
        ordering = [
            '-date_created'
        ]


class CompleteOrder(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.DO_NOTHING, related_name="com_orders",
                             verbose_name=_("کاربر"))
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING, verbose_name=_("محصول"))
    price = models.BigIntegerField(default=0, verbose_name=_("قیمت کل"))
    date_created = models.DateTimeField(auto_now=False, auto_now_add=False, verbose_name=_("تاریخ ایجاد"))

    def __str__(self):
        return self.user.username + f" #{self.id} "

    class Meta:
        verbose_name = _("سبد خرید")
        verbose_name_plural = _("سبد خرید پرداخت شده")
        ordering = [
            '-date_created'
        ]
