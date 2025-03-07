import json
import websockets
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import TradeData

BINANCE_WS_URL = "wss://stream.binance.com:9443/ws/btcusdt@trade"
PAIR = "ETH/USDT"

class BinanceConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.listen_to_binance()

    async def disconnect(self, close_code):
        pass

    async def listen_to_binance(self):
        async with websockets.connect(BINANCE_WS_URL) as ws:
            while True:
                data = await ws.recv()
                trade_data = json.loads(data)
                
                price = trade_data["p"]

                await self.save_trade_data(price)
                
                await self.send(text_data=json.dumps({
                    "pair": PAIR,
                    "price": price,
                }))

                await asyncio.sleep(60)

    async def save_trade_data(self, price):
        trade = TradeData(
            pair=PAIR,
            price=price,
        )
        await database_sync_to_async(trade.save)()
