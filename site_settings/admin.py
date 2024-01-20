from django.contrib import admin
from site_settings.models import SiteSetting, QuestionPrice

# Register your models here.

admin.site.register(SiteSetting)
admin.site.register(QuestionPrice)
