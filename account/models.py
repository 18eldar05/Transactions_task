import uuid
from django.db import models


class Account(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=100)
    balance = models.DecimalField(max_digits=11, decimal_places=2)


class AccountInfo(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    account_id = models.OneToOneField('Account', on_delete=models.PROTECT)
    full_name = models.CharField(max_length=300)
    address = models.TextField()


class Transactions(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    account_id = models.ForeignKey('Account', on_delete=models.PROTECT)
    amount = models.DecimalField(max_digits=11, decimal_places=2)
