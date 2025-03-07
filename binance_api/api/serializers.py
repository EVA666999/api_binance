from rest_framework import serializers
from .models import TradeData

class TradeDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = TradeData
        fields = ['pair', 'price']