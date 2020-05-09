from django.shortcuts import render
from django.http import HttpResponse, Http404

from .load_data import load_data, load_name
from .models import Wallet_indentificator, Wallet_value


def get_date(request, wallet_name_):
    print('get_date')
    wallet = Wallet_indentificator.objects.get(wallet_name=wallet_name_)
    wallet_values = Wallet_value.objects.filter(wallet=wallet).order_by(
        '-date')[:10]
    dates = []
    for i in wallet_values:
        dates += [str(i.date)]
    return render(request, 'Wallet/choose_date.html',
                  {'wallet': wallet, 'dates_in_memory': dates})


def add_date(request, wallet_name_):
    date_ = '-'.join(request.POST['date'].split('/')[::-1])
    wallet = Wallet_indentificator.objects.get(wallet_name=wallet_name_)
    try:
        load_data(request.POST['date'])
        wallet_info = Wallet_value.objects.get(wallet=wallet, date=date_)
        return render(request, 'Wallet/wallet.html',
                      {'wallet': wallet, 'wallet_info': wallet_info})
    except:
        return HttpResponse('Нет данных на этот день')


def show_wallet(request, wallet_name_, wallet_date_=None):
    if wallet_date_ is None:
        date_ = '-'.join(request.POST['date'].split('/')[::-1])
    else:
        date_ = wallet_date_
    wallet = Wallet_indentificator.objects.get(wallet_name=wallet_name_)
    try:
        wallet_info = Wallet_value.objects.get(wallet=wallet, date=date_)
        return render(request, 'Wallet/wallet.html',
                      {'wallet': wallet, 'wallet_info': wallet_info})
    except:
        return add_date(request, wallet_name_)


def main_page(request):
    wallet_names = []
    wallets_list = Wallet_indentificator.objects.all().order_by('wallet_name')
    if len(wallets_list) == 0:
        load_name()
        wallets_list = Wallet_indentificator.objects.all()
    for wallet in wallets_list:
        wallet_names += [wallet.wallet_name]
    return render(request, 'Wallet/list.html',
                  {'wallets_list': wallet_names})
