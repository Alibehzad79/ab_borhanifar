from django.contrib import admin
from site_settings.models import SiteSetting, Seo, AboutMe, SocialNetwork


# Register your models here.

class SocialNetworkInline(admin.TabularInline):
    model = SocialNetwork


@admin.register(AboutMe)
class AboutMeAdmin(admin.ModelAdmin):
    list_display = ['name']
    inlines = [SocialNetworkInline]


admin.site.register(SiteSetting)
admin.site.register(Seo)
