from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from mini_wallet.models import WalletUser, Wallet, Deposit


class WalletUserSerializer(serializers.ModelSerializer):
    customer_xid = serializers.UUIDField(required=True, write_only=True, validators=[UniqueValidator(queryset=WalletUser.objects.all())])

    class Meta:
        model = WalletUser
        fields = ('customer_xid',)


class WalletSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()

    def get_status(self, wallet):
        if wallet.status:
            return "enabled"
        return "disabled"

    class Meta:
        model = Wallet
        fields = '__all__'


class DisableWalletSerializer(serializers.Serializer):
    is_disabled = serializers.BooleanField(required=True)


class AddMoneySerializer(serializers.ModelSerializer):
    amount = serializers.IntegerField(required=True)
    reference_id = serializers.UUIDField(required=True, validators=[UniqueValidator(queryset=Deposit.objects.all())])
    # status = serializers.SerializerMethodField()

    # def get_status(self, add_money):
    #     import pdb;pdb.set_trace()
    #     if add_money.status:
    #         return "success"
    #     return "failed"

    class Meta:
        model = Deposit
        fields = '__all__'

class WithdrawMoneySerializer(serializers.ModelSerializer):
    amount = serializers.IntegerField(required=True)
    reference_id = serializers.UUIDField(required=True, validators=[UniqueValidator(queryset=Deposit.objects.all())])
    # status = serializers.SerializerMethodField()

    # def get_status(self, add_money):
    #     import pdb;pdb.set_trace()
    #     if add_money.status:
    #         return "success"
    #     return "failed"

    class Meta:
        model = Deposit
        fields = '__all__'