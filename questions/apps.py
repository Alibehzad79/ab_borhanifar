from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class QuestionsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'questions'
    verbose_name = _("بخش سوالات")
