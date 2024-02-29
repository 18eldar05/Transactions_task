from rest_framework import serializers
from .models import *


class AccountInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountInfo
        fields = '__all__'


class TransactionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transactions
        fields = '__all__'


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'
