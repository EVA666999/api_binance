from .serializers import TradeDataSerializer
from .models import TradeData
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend

class TradeDataViewset(viewsets.ReadOnlyModelViewSet):
    queryset = TradeData.objects.all()
    serializer_class = TradeDataSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ['pair']