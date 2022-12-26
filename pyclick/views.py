from django.http import JsonResponse
from django.shortcuts import redirect
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView

from participant.serializers import ParticipantSerializer
from . import serializers
from .methods_merchant_api import Services
from .models import ClickTransaction
from .status import (ORDER_FOUND, INVALID_AMOUNT, ORDER_NOT_FOUND)
from .utils import PyClickMerchantAPIView


class TransactionCheck(PyClickMerchantAPIView):
    @classmethod
    def check_order(cls, order_id: str, amount: str):
        if order_id:
            try:
                order = ClickTransaction.objects.get(id=order_id)
                if int(amount) == order.amount:
                    return ORDER_FOUND
                else:
                    return INVALID_AMOUNT
            except ClickTransaction.DoesNotExist:
                return ORDER_NOT_FOUND

    @classmethod
    def successfully_payment(cls, transaction: ClickTransaction):
        """Success transaction callback"""
        serializer = ParticipantSerializer(data=transaction.participant_data)
        if serializer.is_valid():
            serializer.save()


class ClickTransactionTestView(PyClickMerchantAPIView):
    VALIDATE_CLASS = TransactionCheck


class ClickMerchantServiceView(APIView):
    def post(self, request, service_type, *args, **kwargs):
        service = Services(request.POST, service_type)
        response = service.api()
        return JsonResponse(response)
