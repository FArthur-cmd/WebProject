from django.urls import path

from . import views

app_name = "Wallet"

urlpatterns = [
    path('main/<str:wallet_name_>/', views.get_date,
         name='get_date'),
    path('main/', views.main_page, name='main_page'),
    path('main/<str:wallet_name_>/show_wallet/',
         views.show_wallet,
         name='show_wallet'),
    path('main/<str:wallet_name_>/<str:wallet_date_>/show_wallet/',
         views.show_wallet,
         name='show_wallet')
]
