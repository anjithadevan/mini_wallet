from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid
# Create your models here.


class WalletUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)


class Wallet(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owned_by = models.ForeignKey(WalletUser, on_delete=models.CASCADE,)
    status = models.BooleanField(default=False)
    enabled_at = models.DateTimeField()
    disabled_at = models.DateTimeField()
    balance = models.IntegerField(default=0)

    def __str__(self):
        return self.owned_by


class Deposit(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    deposited_by = models.ForeignKey(WalletUser, on_delete=models.CASCADE,)
    status = models.BooleanField(default=False)
    deposited_at = models.DateTimeField(auto_now_add=True)
    amount = models.IntegerField()
    reference_id = models.UUIDField(unique=True)


class Withdrawal(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    withdrawn_by = models.ForeignKey(WalletUser, on_delete=models.CASCADE,)
    status = models.BooleanField(default=False)
    withdrawn_at = models.DateTimeField(auto_now_add=True)
    amount = models.IntegerField()
    reference_id = models.UUIDField(unique=True)