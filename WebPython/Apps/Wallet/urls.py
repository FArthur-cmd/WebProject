from django.urls import path

from . import views

app_name = "Wallet"

urlpatterns = [
    path('<str:wallet_name_>/', views.get_date,
         name='get_date'),
    path('', views.main_page, name='main_page'),
    path('<str:wallet_name_>/show_wallet/',
         views.show_wallet,
         name='show_wallet'),
    path('<str:wallet_name_>/<str:wallet_date_>/show_wallet/',
         views.show_wallet,
         name='show_wallet')
]
