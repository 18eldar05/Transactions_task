import decimal
from rest_framework import generics, status
from .models import *
from .serializers import TransactionsSerializer, AccountSerializer, AccountInfoSerializer
from rest_framework.response import Response
from django.http import Http404
from django.db import transaction


class AccountAPIList(generics.ListCreateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer


class AccountAPIDetailView(generics.RetrieveAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer


class TransactionsAPIDetailView(generics.RetrieveAPIView):
    queryset = Transactions.objects.all()
    serializer_class = TransactionsSerializer


class TransactionsAPIList(generics.ListCreateAPIView):
    queryset = Transactions.objects.all()
    serializer_class = TransactionsSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        with transaction.atomic():
            self.perform_create(serializer)
            instance = Account.objects.get(pk=serializer.data["account_id"])
            instance.balance += decimal.Decimal(serializer.data["amount"])
            instance.save()

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class AccountTransactionsAPIList(generics.ListCreateAPIView):
    queryset = Transactions.objects.all()
    serializer_class = TransactionsSerializer

    def list(self, request, *args, **kwargs):
        pk = kwargs["pk"]
        try:
            queryset = Transactions.objects.filter(account_id=pk)
        except Transactions.DoesNotExist:
            raise Http404("No account_id found!")

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class AccountInfoAPIList(generics.RetrieveUpdateDestroyAPIView):
    queryset = AccountInfo.objects.all()
    serializer_class = AccountInfoSerializer

    def get_account_info_object(self, pk):
        try:
            instance = AccountInfo.objects.get(account_id=pk)
        except AccountInfo.DoesNotExist:
            raise Http404("No account_id found!")
        return instance

    def get(self, request, *args, **kwargs):
        instance = self.get_account_info_object(kwargs["pk"])
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        pk = kwargs["pk"]
        try:
            request.data['account_id'] = Account.objects.get(pk=pk).pk
        except Account.DoesNotExist:
            raise Http404("No account found!")

        serializer = AccountInfoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        instance = self.get_account_info_object(kwargs["pk"])
        serializer = AccountInfoSerializer(data=request.data, instance=instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        instance = self.get_account_info_object(kwargs["pk"])
        serializer = AccountInfoSerializer(data=request.data, instance=instance, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
