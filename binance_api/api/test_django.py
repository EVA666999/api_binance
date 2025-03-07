import pytest
from rest_framework.test import APIClient
from rest_framework import status
from api.models import TradeData
from django.urls import reverse


@pytest.mark.django_db
def test_trade_data_viewset():
    TradeData.objects.all().delete()

    TradeData.objects.create(pair="BTC/USDT", price="50000")
    TradeData.objects.create(pair="ETH/USDT", price="4000")

    client = APIClient()

    url = reverse('trade-data-list')
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    assert len(response.data) == 2, f"Ожидалось 2 объекта, получено {len(response.data)}"

    pairs = {item['pair'] for item in response.data}
    prices = {item['price'] for item in response.data}
    assert pairs == {"BTC/USDT", "ETH/USDT"}

    assert "50000.00000000" in prices
    assert "4000.00000000" in prices