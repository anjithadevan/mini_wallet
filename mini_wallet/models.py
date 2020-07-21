from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid


# Create your models here.


class WalletUser(AbstractUser):
    """
    AbstractUser is inherited to change the id field to UUIDField
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer_xid = models.UUIDField(default=uuid.uuid4, null=False, blank=False)


class Wallet(models.Model):
    """
    Wallet Informations
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owned_by = models.ForeignKey(WalletUser, on_delete=models.CASCADE, )
    status = models.BooleanField(default=False)
    enabled_at = models.DateTimeField(null=True)
    disabled_at = models.DateTimeField(null=True)
    balance = models.IntegerField(default=0)


class Transaction(models.Model):
    """"
    Transaction details(Depositing and withdrawal of money)
    """
    DEPOSIT = 'DT'
    WITHDRAWAL = 'WT'
    TRANSACTION_CHOICES = [(DEPOSIT, 'Deposit'), (WITHDRAWAL, 'Withdrawal')]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    deposited_or_withdrawn_by = models.ForeignKey(WalletUser, on_delete=models.CASCADE, )
    status = models.BooleanField(default=False)
    deposited_or_withdrawn_at = models.DateTimeField(auto_now_add=True)
    amount = models.IntegerField()
    reference_id = models.UUIDField(unique=True)
    transaction_status = models.CharField(max_length=2, choices=TRANSACTION_CHOICES)
