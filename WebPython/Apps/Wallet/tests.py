from __future__ import absolute_import

import requests
from bs4 import BeautifulSoup
from django.test import TestCase

from .load_data import load_data
from .models import Wallet_value, Wallet_indentificator


# Create your tests here.
class TestModelCreating(TestCase):
    def setUp(self) -> None:
        example = Wallet_indentificator(
            wallet_name="Testing",
            wallet_id="TEST_ID",
            wallet_char_code="TestChar"
        )
        example.save()
        example_value = Wallet_value(
            wallet=example,
            wallet_nominal=1,
            wallet_value=3.3,
            date="2020-05-05"
        )
        example_value.save()
        example_value = Wallet_value(
            wallet=example,
            wallet_nominal=2,
            wallet_value=5.3,
            date="2021-05-05"
        )
        example_value.save()

    def test_correct_addition(self):
        wallet = Wallet_indentificator.objects.get(wallet_name="Testing")
        wallet_array = Wallet_indentificator.objects.filter(
            wallet_name="Testing")
        self.assertEqual(len(wallet_array), 1)
        self.assertEqual(wallet.wallet_name, "Testing")
        self.assertEqual(wallet.wallet_id, "TEST_ID")
        self.assertEqual(wallet.wallet_char_code, "TestChar")
        wallet_value = Wallet_value.objects.filter(
            wallet=wallet)
        self.assertEqual(len(wallet_value), 2)
        Wallet_indentificator.objects.filter(
            wallet_name="Testing").delete()
        wallet_array = Wallet_indentificator.objects.filter(
            wallet_name="Testing")
        self.assertEqual(len(wallet_array), 0)
        wallet_value = Wallet_value.objects.filter(
            wallet=wallet)
        self.assertEqual(len(wallet_value), 0)


class TestSomeData(TestCase):
    def setUp(self) -> None:
        load_data("01/05/2020")
        wallet = Wallet_indentificator.objects.all()[0]
        wallet_value_list = Wallet_value.objects.filter(wallet=wallet)
        wallet_value = wallet_value_list[0]
        self.date = (str(wallet_value.date))
        date = '/'.join(self.date.split('-')[::-1])
        req = requests.get("http://www.cbr.ru/scripts/XML_daily.asp?date_req=" +
                           date)
        soup = BeautifulSoup(req.content, 'lxml')
        self.valutes = soup.find_all('valute')

    def test_date(self):
        for valute in self.valutes:
            wallet = Wallet_indentificator.objects.get(wallet_name=
                                                       valute.find(
                                                           'name').text)
            wallet_value = Wallet_value.objects.get(wallet=wallet,
                                                    date=self.date)
            self.assertEqual(wallet_value.wallet_value, float(
                '.'.join(valute.find('value').text.split(','))))
            self.assertEqual(wallet_value.wallet_nominal, int(valute.find(
                'nominal').text))


