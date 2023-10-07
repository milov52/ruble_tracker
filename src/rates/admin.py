from django.contrib import admin

from .models import Currency, Rate


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ("id", "char_code", "name")


@admin.register(Rate)
class RateAdmin(admin.ModelAdmin):
    list_display = ("date", "currency", "value")
    list_filter = ("currency",)
