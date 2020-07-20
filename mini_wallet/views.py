from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED, HTTP_400_BAD_REQUEST, HTTP_201_CREATED
from rest_framework.authtoken.models import Token
from mini_wallet.models import WalletUser, Wallet
from mini_wallet.serializers import WalletUserSerializer, WalletSerializer


class InitializeAccountViewSet(viewsets.ModelViewSet):
    """
    Creates the user and wallet
    """
    permission_classes = (AllowAny,)
    queryset = WalletUser.objects.all()
    serializer_class = WalletUserSerializer

    def create(self, request, *args, **kwargs):
        serializer = WalletUserSerializer(data=request.data)
        if serializer.is_valid():
            customer_xid = serializer.validated_data['customer_xid']
            user = WalletUser.objects.create_user(username=customer_xid, customer_xid=customer_xid)
            if user:
                token, _ = Token.objects.get_or_create(user=user)
                return response('success', {"token": token.key}, HTTP_200_OK)
            return response('failed', {}, HTTP_401_UNAUTHORIZED)
        else:
            return Response(
                serializer.errors,
                status=HTTP_400_BAD_REQUEST
            )


class WalletViewSet(viewsets.ModelViewSet):
    """
    Creates the wallet,get wallet list and status changing
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer

    def list(self, request, *args, **kwargs):
        user = self.request.user
        queryset = Wallet.objects.filter(owned_by=user)
        serializer = self.get_serializer(queryset, many=True)
        return response('success', {"wallet": serializer.data}, HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        request.data['owned_by'] = self.request.user.id
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            wallet, _ = Wallet.objects.get_or_create(owned_by=self.request.user)
            if wallet.status:
                return response('failed', {"message": 'already enabled'}, HTTP_400_BAD_REQUEST)
            else:
                serializer.validated_data['status'] = wallet.status = True
                wallet.save()
                return response('success', {'wallet': serializer.data}, HTTP_201_CREATED)
        return response('failed', serializer.errors, HTTP_400_BAD_REQUEST)


def response(status, data, code):
    responses = {
        'status': status,
        'data': data
    }
    return Response(data=responses, status=code)