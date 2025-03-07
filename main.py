import websocket
from websocket import WebSocketApp


def on_message(_wsa, message):
    print(message)

def on_error(_wsa, error):
    print(f"Error: {error}")

def on_close(_wsa, close_status_code, close_msg):
    print("### Closed ###")

def on_open(_wsa):
    print("Connection opened")

def run():
    stream_name = 'btcusdt@depth'
    wss = 'wss://stream.binance.com:9443/ws/btcusdt@trade'

    wsa = websocket.WebSocketApp(
        wss,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close
    )
    wsa.on_open = on_open
    wsa.run_forever()

if __name__ == "__main__":
    run()
