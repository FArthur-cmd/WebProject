from .models import Wallet_value, Wallet_indentificator


def clear_repeated_date():
    wallets = Wallet_indentificator.objects.all()
    for wallet in wallets:
        list_to_delete = []
        print(wallet.wallet_name)
        values_list = Wallet_value.objects.filter(wallet=wallet)
        print(len(values_list))
        for i in range(len(values_list)):
            for j in range(i + 1, len(values_list)):
                if values_list[i].date == values_list[j].date and i != j:
                    list_to_delete += [values_list[j]]
                    print(values_list[j].date, i, j)
        for i in list_to_delete:
            try:
                i.delete()
            except:
                pass
