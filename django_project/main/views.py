import requests

from django.shortcuts import render
from django.http import HttpResponse

# Model
from django.db.models import Q

# Auth
from django.contrib.auth import authenticate
from django.contrib.auth import login, logout

# Serializer
from .serializers import CreateWalletSerializer

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

        # Execute the command
        command = 'node . wallet new'
        output = subprocess.check_output(command.split())
        print(output)

        return Response({"status": 1, "message": output}, status=status.HTTP_200_OK)

    else:
        return Response({"status": 0, "message": [str(serializer), serializer.errors]},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)
