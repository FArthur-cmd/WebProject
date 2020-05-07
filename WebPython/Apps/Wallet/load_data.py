import requests
from bs4 import BeautifulSoup

from .models import Wallet_value, Wallet_indentificator


def load_data(date_):
    print("load data")
    req = requests.get("http://www.cbr.ru/scripts/XML_daily.asp?date_req=" +
                       date_)
    soup = BeautifulSoup(req.content, 'lxml')
    wallets = Wallet_indentificator.objects.all()
    if date_.split('/') == str(soup.find('valcurs')['date']).split('.'):
        ids = soup.find_all('valute')
        for i in ids:
            print(i)
            wallet = wallets[ids.index(i)]
            print(wallet.wallet_name)
            data = Wallet_value(
                wallet=wallet,
                wallet_nominal=int(i.find('nominal').text),
                wallet_value=float(".".join(i.find('value').text.split(','))),
                date='-'.join(soup.find('valcurs')['date'].split('.')[::-1])
            )
            data.save()
            print(data.wallet_nominal)
            print(data.wallet_value)
    else:
        raise ValueError


def load_name():
    req = requests.get("http://www.cbr.ru/scripts/XML_daily.asp?date_req=03"
                       "/03/2020")
    soup = BeautifulSoup(req.content, 'lxml')
    ids = soup.find_all('valute')
    for i in ids:
        a = Wallet_indentificator(
            wallet_name=i.find('name').text,
            wallet_id=i['id'],
            wallet_char_code=i.find('charcode').text,
        )
        a.save()
