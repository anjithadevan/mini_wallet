from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from mini_wallet.models import WalletUser, Wallet


class WalletUserSerializer(serializers.ModelSerializer):
    customer_xid = serializers.UUIDField(required=True, write_only=True, validators=[UniqueValidator(queryset=WalletUser.objects.all())])

    class Meta:
        model = WalletUser
        fields = ('customer_xid',)


class WalletSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()

    def get_status(self, wallet):
        if wallet['status']:
            return "enabled"
        return "disabled"

    class Meta:
        model = Wallet
        fields = '__all__'