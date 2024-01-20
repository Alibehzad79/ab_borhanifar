from django.contrib import admin
from orders.models import Order, CompleteOrder


# Register your models here.


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["__str__", 'user', "product", "date_created", "is_pay"]
    list_editable = ["is_pay"]
    list_filter = ["date_created", "is_pay"]
    list_display_links = ["__str__", "user", "product"]
    search_fields = ["user__username", "user__email", "product__title"]


@admin.register(CompleteOrder)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["__str__", "user", "date_created"]
    list_filter = ["date_created"]
    list_display_links = ["__str__", "user"]
    search_fields = ["user__username", "user__email"]
