from django.db import models


class Wallet_indentificator(models.Model):
    wallet_name = models.CharField('Название валюты', max_length=200)
    wallet_id = models.CharField('ID', max_length=20)
    wallet_char_code = models.CharField('Char_code', max_length=10)

    class Meta:
        verbose_name = 'Валюта'
        verbose_name_plural = 'Валюты'


class Wallet_value(models.Model):
    wallet = models.ForeignKey(Wallet_indentificator,
                               on_delete=models.CASCADE)
    wallet_nominal = models.IntegerField('Nominal')
    wallet_value = models.FloatField('Value')
    date = models.DateField("Data")

    class Meta:
        verbose_name = 'Курс валюты'
        verbose_name_plural = 'Курс валют'
