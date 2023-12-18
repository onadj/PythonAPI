# serializers.py
from rest_framework import serializers
from .models import Receipt, Transaction, Refund

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'

class RefundSerializer(serializers.ModelSerializer):
    class Meta:
        model = Refund
        fields = '__all__'

class ReceiptSerializer(serializers.ModelSerializer):
    transactions = TransactionSerializer(many=True)
    refunds = RefundSerializer(many=True)

    class Meta:
        model = Receipt
        fields = '__all__'
