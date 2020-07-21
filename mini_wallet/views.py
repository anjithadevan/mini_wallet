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
from rest_framework.views import APIView

from mini_wallet.models import WalletUser, Transaction, Wallet
from mini_wallet.serializers import WalletUserSerializer, WalletSerializer, DisableWalletSerializer, \
    TransactionSerializer
from datetime import datetime


class InitializeAccountViewSet(viewsets.ModelViewSet):
    """
    Creates the user
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


class WalletView(APIView):
    """
    APIView for getting wallet details, enabling and disabling wallet
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        user = self.request.user
        wallet = Wallet.objects.filter(owned_by=user, status=True)
        if wallet:
            serializer = WalletSerializer(wallet, many=True)
            return response('success', {"wallet": serializer.data}, HTTP_200_OK)
        return response('failed', {"error": 'Disabled'}, HTTP_400_BAD_REQUEST)

    def post(self, request, format=None):
        request.data['owned_by'] = self.request.user.id
        serializer = WalletSerializer(data=request.data)
        if serializer.is_valid():
            wallet, _ = Wallet.objects.get_or_create(owned_by=self.request.user)
            if wallet.status:
                return response('fail', {"error": "Already enabled"}, HTTP_400_BAD_REQUEST)
            else:
                serializer.validated_data['status'] = wallet.status = True
                wallet.enabled_at = datetime.now()
                wallet.save()
                serializer = WalletSerializer(instance=wallet)
                return response('success', {'wallet': serializer.data}, HTTP_201_CREATED)
        return response('failed', serializer.errors, HTTP_400_BAD_REQUEST)

    def patch(self, request):
        wallet = Wallet.objects.get(owned_by=self.request.user)
        serializer = DisableWalletSerializer(wallet, data=request.data)
        if serializer.is_valid():
            wallet.status = False
            wallet.disabled_at = datetime.now()
            wallet.save()
            serializer = WalletSerializer(instance=wallet)
            return response('success', {'wallet': serializer.data}, HTTP_201_CREATED)
        return response('failed', serializer.errors, HTTP_400_BAD_REQUEST)


class AddvirtualMoneyViewSet(viewsets.ModelViewSet):
    """
    Viewset for adding money to the wallet
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = TransactionSerializer
    queryset = Transaction.objects.all()

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data['deposited_or_withdrawn_by'] = self.request.user.id
        data['status'] = True
        data['transaction_status'] = 'DT'
        serializer = TransactionSerializer(data=data)
        if serializer.is_valid():
            try:
                wallet = Wallet.objects.get(owned_by=self.request.user)
                if wallet.status:
                    self.perform_create(serializer)
                    wallet.balance = wallet.balance + serializer.data['amount']
                    wallet.save()
                    return response('success', {'deposit': get_data('deposited_by', 'deposited_at', serializer.data)},
                                    HTTP_201_CREATED)
                else:
                    return response('failed', {'message': 'wallet is not yet enabled'}, HTTP_400_BAD_REQUEST)
            except ObjectDoesNotExist:
                return response('failed', {'message': 'No wallet is found'}, HTTP_400_BAD_REQUEST)
        else:
            return response('failed', serializer.errors, HTTP_400_BAD_REQUEST)


class WithdrawVirtualMoneyViewSet(viewsets.ModelViewSet):
    """
    Viewset for money withdrawal from wallet
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = TransactionSerializer
    queryset = Transaction.objects.all()

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data['deposited_or_withdrawn_by'] = self.request.user.id
        data['status'] = True
        data['transaction_status'] = 'WT'
        serializer = TransactionSerializer(data=data)
        if serializer.is_valid():
            wallet = Wallet.objects.get(owned_by=self.request.user)
            if wallet.status:
                if wallet.balance - serializer.validated_data['amount'] >= 0:
                    wallet.balance = wallet.balance - serializer.validated_data['amount']
                    wallet.save()
                    self.perform_create(serializer)
                    return response('success',
                                    {'withdrawal': get_data('withdrawn_by', 'withdrawn_at', serializer.data)},
                                    HTTP_201_CREATED)
                else:
                    return response('failed', {'message': "wallet doesn't have enough money"}, HTTP_400_BAD_REQUEST)
            else:
                return response('failed', {'message': "wallet is not yet enabled"}, HTTP_400_BAD_REQUEST)
        else:
            return response('failed', serializer.errors, HTTP_400_BAD_REQUEST)


def response(status, data, code):
    responses = {
        'status': status,
        'data': data
    }
    return Response(data=responses, status=code)


def get_data(user_by, time, serializer_data):
    status = 'failed'
    if serializer_data['status']:
        status = 'success'
    data = {
        'id': serializer_data['id'],
        user_by: serializer_data['deposited_or_withdrawn_by'],
        'status': status,
        time: serializer_data['deposited_or_withdrawn_at'],
        'amount': serializer_data['amount'],
        'reference_id': serializer_data['reference_id'],
    }
    return data
