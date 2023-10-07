from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

class Currency(models.Model):
    char_code = models.CharField(max_length=3)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.char_code} - {self.name}"


class Rate(models.Model):
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    date = models.DateField()
    value = models.DecimalField(decimal_places=2, max_digits=10)

    def __str__(self):
        return f"Курс на {self.date} у {self.currency} - {self.value}"

class UserCurrencyTracking(models.Model):
    user = models.ForeignKey(CustomUser, verbose_name='Пользователь', on_delete=models.CASCADE)
    currency = models.ForeignKey(Currency, verbose_name='Котируемая валюта', on_delete=models.CASCADE)
    threshold = models.FloatField(verbose_name='Пороговое значение цены')

    def __str__(self):
        return self.currency.name