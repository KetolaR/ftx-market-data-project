import websocket
import json
from insert import insert_trade
import datetime

def on_open(ws):
    print('opened')

    auth_data = {
        'op': 'subscribe',
        'channel': 'trades',
        'market': 'BTC-PERP'
    }
    ws.send(json.dumps(auth_data))

def on_message(ws, message):
    message = json.loads(message)
    insert_trade(message)


def on_close(ws):
    print('closed connection')


socket = 'wss://ftx.com/ws/'
ws = websocket.WebSocketApp(socket,
                            on_open=on_open,
                            on_message=on_message,
                            on_close=on_close)

ws.run_forever()