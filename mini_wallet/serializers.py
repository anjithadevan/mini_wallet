from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from mini_wallet.models import WalletUser, Wallet, Transaction


class WalletUserSerializer(serializers.ModelSerializer):
    """
    wallet user serializer
    """
    customer_xid = serializers.UUIDField(required=True, write_only=True,
                                         validators=[UniqueValidator(queryset=WalletUser.objects.all())])

    class Meta:
        model = WalletUser
        fields = ('customer_xid',)


class WalletSerializer(serializers.ModelSerializer):
    """
    wallet serializer for getting wallet details
    """
    status = serializers.SerializerMethodField()

    def get_status(self, wallet):
        if wallet.status:
            return "enabled"
        return "disabled"

    class Meta:
        model = Wallet
        fields = '__all__'


class DisableWalletSerializer(serializers.Serializer):
    """
    wallet serializer for disabling wallet
    """
    is_disabled = serializers.BooleanField(required=True)


class TransactionSerializer(serializers.ModelSerializer):
    """
    Serializer for add and withdrawal money
    """
    amount = serializers.IntegerField(required=True)
    reference_id = serializers.UUIDField(required=True, validators=[UniqueValidator(queryset=Transaction.objects.all())])

    class Meta:
        model = Transaction
        fields = '__all__'
