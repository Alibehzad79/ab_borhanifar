from django.db import models
from django.utils.translation import gettext_lazy as _


# Create your models here.

class Product(models.Model):
    title = models.CharField(max_length=100, verbose_name=_("عنوان محصول"))
    description = models.TextField(verbose_name=_("توضیحات کوتاه محصول"))
    image = models.ImageField(upload_to="images/", verbose_name=_("تصویر محصول"))
    file = models.FileField(upload_to="products/files/", verbose_name=_("فایل (محصول)"), default=None)
    price = models.BigIntegerField(default=0, verbose_name=_("قیمت محصول(تومان)"))

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("محصول")
        verbose_name_plural = _("محصولات")
