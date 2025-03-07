from django.urls import path
from rest_framework import routers
from .views import TradeDataViewset


trade = routers.DefaultRouter()

trade.register(r'trade', TradeDataViewset, basename='trade-data')
