from django.urls import path
from . import views as main_views

urlpatterns = [
    path('api/create_user_wallet/', main_views.api_create_wallet, name='api_create_wallet'),
]
