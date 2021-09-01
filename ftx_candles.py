import requests
import json
import time

class FTXCandles(object):
    """Retrieves historical market data in the form of candles from ftx.com."""

    _limit = 5000
    _ENDPOINT = 'https://ftx.com/api/markets/'
    _minute = 60
    _month = 60*60*24*365

    def __init__(
        self, trade_pair = 'BTC-PERP', candle_resolution = _minute, history_length = _month,
        current_time = time.time()
        ):
        self.time = current_time
        self.market_name = trade_pair
        self.resolution = candle_resolution
        self.history_length = history_length
        self._params() # initialize the parameters of the get request

    def _params(self):
        self.parameters = {
            "market_name": self.market_name,
            "resolution": self.resolution,
            "start_time": self.time - self.history_length,
            "end_time": self.time,
            "limit": self._limit
        }

    def get_candles(self):
        self.results = []
        while True:
            # get request
            response = requests.get(self._ENDPOINT + self._path(self.market_name),\
                params=self.parameters).json()
            if response['success'] == False:
                print("Error occured during 'get' request")
                break
            response = response['result']

            # avoid dupes using unique timestamp of each candle
            time_ids = set()
            deduped_trades = [r for r in response if r['time'] not in time_ids]

            if len(self.results)==0:
                self.results = deduped_trades
            else:
                self.results = deduped_trades + self.results

            time_ids |= {r['time'] for r in deduped_trades}

            # pagination
            self.parameters['end_time'] = min(r['time'] for r in response)/1000

            if len(response) < self._limit: # if we have <limit candles left
                break                       # then we are done paginating

        return self.results # a list of dictionaries

    def _path(self, market_name):
        "constructs a valid path given the market name"
        return f"{market_name}/candles"

if __name__ == '__main__':
    x=FTXCandles(trade_pair = 'BTC-PERP', candle_resolution = 60, history_length = 240,
        current_time = time.time())
    resp = x.getCandles()
    print(resp)
