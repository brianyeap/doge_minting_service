from django.urls import path
from . import views as main_views

urlpatterns = [
    path('api/create_user_wallet/', main_views.api_create_wallet, name='api_create_wallet'),
    path('api/query_bal/', main_views.api_query_bal, name='api_query_bal'),
]
