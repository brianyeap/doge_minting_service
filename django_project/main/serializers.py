from rest_framework import serializers
from rest_framework import authentication
from rest_framework import exceptions
from django.utils.translation import gettext_lazy as _

from django.contrib.auth import authenticate

from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator


class CreateWalletSerializer(serializers.Serializer):
    count = serializers.IntegerField()


class QueryBalanceSerializer(serializers.Serializer):
    wallet_data = serializers.CharField(max_length=500)


class MintNFTSerializer(serializers.Serializer):
    file_name = serializers.CharField(max_length=100)
    base64 = serializers.CharField(max_length=1000000000)


class SendFundsSerializer(serializers.Serializer):
    quantity = serializers.FloatField()
    wallet_data = serializers.CharField(max_length=500)
    receiver_address = serializers.CharField(max_length=100)
