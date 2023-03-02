import requests
import json
import ast

from django.shortcuts import render
from django.http import HttpResponse

# Model
from django.db.models import Q

# Auth
from django.contrib.auth import authenticate
from django.contrib.auth import login, logout

# Serializer
from .serializers import CreateWalletSerializer, QueryBalance

# API
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import authentication_classes, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token

# Exception
from django.core.exceptions import ObjectDoesNotExist

# Settings
from django.conf import settings

# Timezone
from datetime import timezone

import os
import subprocess


# Create your views here.

@api_view(['POST'])
def api_create_wallet(request):
    serializer = CreateWalletSerializer(data=request.data)
    if serializer.is_valid():
        # Navigate to the doginals directory
        directory_path = '/home/semi/Desktop/doginals'
        os.chdir(directory_path)

        # Create wallet
        command = 'node . wallet new'
        output = subprocess.check_output(command.split(), stderr=subprocess.STDOUT)

        if "wallet already exists" in str(output):
            command = 'rm -rf .wallet.json'
            subprocess.check_output(command.split(), stderr=subprocess.STDOUT)

            command = 'node . wallet new'
            subprocess.check_output(command.split(), stderr=subprocess.STDOUT)

            command = 'cat .wallet.json'
            output = subprocess.check_output(command.split())

        return Response({"status": 1, "message": output}, status=status.HTTP_200_OK)

    else:
        return Response({"status": 0, "message": [str(serializer), serializer.errors]},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def api_query_bal(request):
    serializer = QueryBalance(data=request.data)
    if serializer.is_valid():
        # Navigate to the doginals directory
        directory_path = '/home/semi/Desktop/doginals'
        os.chdir(directory_path)

        # Remove wallet
        command = 'rm -rf .wallet.json'
        subprocess.check_output(command.split(), stderr=subprocess.STDOUT)

        input_dict = ast.literal_eval(serializer.validated_data["wallet_data"])

        # Create the wallet1.json file
        with open(f'.wallet.json', 'w') as f:
            json.dump(input_dict, f, indent=4)

        return Response({"status": 1, "message": "Success"}, status=status.HTTP_200_OK)

    else:
        return Response({"status": 0, "message": [str(serializer), serializer.errors]},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)
