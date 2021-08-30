import websocket
import json
from insert import insert_trade
import datetime



subscription = {
    'op': 'subscribe',
    'channel': 'trades',
    'market': 'BTC-PERP'
}

def on_open(ws):
    print('websocket connection opened')
    ws.send(json.dumps(subscription))

def on_message(ws, message):
    message = json.loads(message)
    insert_trade(message)

def on_close(ws):
    print('closed connection')


if __name__ == '__main__':

    socket = 'wss://ftx.com/ws/'
    ws = websocket.WebSocketApp(socket,
                                on_open=on_open,
                                on_message=on_message,
                                on_close=on_close)

    ws.run_forever()