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
