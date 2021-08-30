import websocket
import json
from insert import insert_trade
from datetime import datetime
import time

class FTXWebsocket(object):
    """Subscribes to ftx.com's websocket stream and listens for trades"""
    
    _SOCKET = 'wss://ftx.com/ws/'

    def __init__(self, trade_pair = 'BTC-PERP'):
        self.subscription = {
            'op': 'subscribe',
            'channel': 'trades',
            'market': trade_pair
        }

    def on_open(self, ws):
        print('Websocket connection opened...')
        ws.send(json.dumps(self.subscription))

    def on_message(self, ws, message):
        message = json.loads(message)
        insert_trade(message, exchange='FTX', processed=False, time_received = datetime.fromtimestamp(time.time()))

    def on_close(self, ws):
        print('closed connection')

    def subscribe(self):
        self.ws = websocket.WebSocketApp(self._SOCKET,
                                    on_open=self.on_open,
                                    on_message=self.on_message,
                                    on_close=self.on_close)
        self.ws.run_forever()


if __name__ == '__main__':

    # socket = 'wss://ftx.com/ws/'
    # ws = websocket.WebSocketApp(socket,
    #                             on_open=on_open,
    #                             on_message=on_message,
    #                             on_close=on_close)

    FTXWebsocket().subscribe()
    
    