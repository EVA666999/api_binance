import asyncio
from channels.testing import WebsocketCommunicator
from django.test import TestCase
from unittest.mock import patch
from api.models import TradeData
from django.db import connection
import pytest
import json
from asgiref.sync import sync_to_async
from unittest.mock import AsyncMock, patch
from api.consumers import BinanceConsumer  # Импортируйте ваш consumer
from asgiref.testing import ApplicationCommunicator
from binance_api.asgi import application  # Импортируйте ваши маршруты для WebSocket
from api.routing import websocket_urlpatterns  # Ваши маршруты для WebSocket

def get_trade_data():
    """Синхронная функция для получения первой записи из базы данных."""
    return TradeData.objects.first()

@pytest.mark.asyncio
@pytest.mark.django_db  
@patch("websockets.connect")
async def test_binance_data_handling(mock_connect):
    mock_connect.return_value.__aenter__.return_value.recv.return_value = json.dumps({
        "p": "50000"
    })

    communicator = WebsocketCommunicator(BinanceConsumer.as_asgi(), "ws://testserver/ws/btcusdt@trade/")
    
    connected, subprotocol = await communicator.connect()
    assert connected, "Соединение не установлено"

    await communicator.send_json_to({"message": "Hello WebSocket"})

    message = await communicator.receive_json_from()
    assert message is not None, "Сообщение не получено"
    assert "pair" in message, "Ключ 'pair' отсутствует в сообщении"
    assert "price" in message, "Ключ 'price' отсутствует в сообщении"
    assert message["pair"] == "ETH/USDT", "Неверное значение для 'pair'"
    assert message["price"] == "50000", "Неверное значение для 'price'"

    saved_trade = await asyncio.to_thread(get_trade_data)
    assert saved_trade is not None, "TradeData не был сохранен в БД"
    assert saved_trade.pair == "ETH/USDT", "Сохраненное значение 'pair' неверное"
    assert float(saved_trade.price) == 50000.0, "Сохраненное значение 'price' неверное"

    await communicator.disconnect()