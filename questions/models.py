from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _


# Create your models here.
class Question(models.Model):
    short_id = models.CharField(max_length=100, verbose_name=_("آیدی سوال"), unique=True, editable=False, blank=True,
                                null=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="questions", verbose_name=_("کاربر"))
    name = models.CharField(max_length=50, verbose_name=_("نام و نام خانوادگی"))
    email = models.EmailField(verbose_name=_("ایمیل"))
    question_title = models.CharField(max_length=100, verbose_name=_("عنوان سوال"), default='')
    question_count = models.IntegerField(default=1, verbose_name=_("تعداد سوال"))
    image = models.ImageField(upload_to="images/questions/", verbose_name=_("تصویر سوال"))
    price = models.CharField(max_length=100, verbose_name=_("هزینه پرداخت شده"))
    is_done = models.BooleanField(default=False, verbose_name=_("پاسخ داد شده / نشده"))
    date_sent = models.DateTimeField(auto_now=False, auto_now_add=False, verbose_name=_("تاریخ ارسال"))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("سوال")
        verbose_name_plural = _("سوالات")
        ordering = [
            '-date_sent'
        ]

    def save(self, *args, **kwargs):
        if self.is_done == True:
            pass
            # TODO send email
        super(Question, self).save(*args, **kwargs)


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="answers")
    image = models.ImageField(upload_to="images/questions/", verbose_name=_("جواب سوال"), blank=True, null=True)

    def __str__(self):
        return self.question.name

    class Meta:
        verbose_name = _("جواب سول")
        verbose_name_plural = _("جواب سوالات")


class QuestionPrice(models.Model):
    price = models.BigIntegerField(default=0, verbose_name=_("قیمت(تومان)"))
    q_count = models.IntegerField(default=10, verbose_name=_("حداکثر تعداد درخواست حل مسئله"))

    def __str__(self):
        return str(self.price)

    class Meta:
        verbose_name = _("تنظیمات بخش حل مسئله")
        verbose_name_plural = verbose_name


class QuestionTitle(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("عنوان سوال"))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("عنوان")
        verbose_name_plural = _("عنوان های سوالات")
