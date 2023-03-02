from django.urls import path
from . import views as main_views

urlpatterns = [
    path('api/get_user_holdings/', main_views.api_create_wallet, name='api_create_wallet'),
]
