from django.urls import path
from . import views as main_views

urlpatterns = [
    path('api/create_user_wallet/', main_views.api_create_wallet, name='api_create_wallet'),
    path('api/query_bal/', main_views.api_query_bal, name='api_query_bal'),
    path('api/query_bal_no_wallet/', main_views.api_query_bal_no_wallet, name='api_query_bal_no_wallet'),
    path('api/mint_nft/', main_views.api_mint_nft, name='api_mint_nft'),
    path('api/mint_nft_other_wallet/', main_views.api_mint_nft_other_wallet, name='api_mint_nft_other_wallet'),
    path('api/send_funds/', main_views.api_send_funds, name='api_send_funds'),
    path('api/send_funds_no_wallet/', main_views.api_send_funds_no_wallet, name='api_send_funds_no_wallet'),
    path('api/empty_wallet/', main_views.api_empty_wallet, name='api_empty_wallet'),
    path('api/split_utxo/', main_views.api_split_utxo, name='api_split_utxo'),
]
