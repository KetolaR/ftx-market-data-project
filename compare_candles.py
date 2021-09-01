import time
from datetime import datetime
import psycopg2
from ftx_candles import FTXCandles
from config import config

def compare_candles(interval, current_interval_timestamp, exchange, trade_pair):
    # allow some time for trades to be logged in database
    time.sleep(10) 

    completed_interval_timestamp = current_interval_timestamp - interval # the previous, now complete, interval
    dt1 = datetime.fromtimestamp(completed_interval_timestamp - 5) # for fetching time from sql table
    dt2 = datetime.fromtimestamp(completed_interval_timestamp + 5)
    window = interval*2

    # fetch candle from API
    fresh_candles = FTXCandles(trade_pair = trade_pair, candle_resolution = interval,
                        history_length=window, current_time = time.time()).get_candles()

    # fetch appropriate candle from SQL database
    command = """
    SELECT time,open,high,low,close,volume FROM candles
    WHERE exchange = %s AND pair = %s AND interval = %s AND time BETWEEN %s AND %s;
    """
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute(command,(exchange, trade_pair, interval, dt1, dt2))
        candle = cur.fetchone()
        cur.close()
        # Log the deltas
        while candle is not None:
            print('\nCandle in database: (constructed from websocket):')
            print('Time:', candle[0], '  Open:', candle[1], '  High:', candle[2])
            print('  Low:', candle[3], '   Close:', candle[4], '  Volume:', candle[5])
            print('\nCandle retrieved from REST API:')
            print('Time:', candle[0], '  Open:', fresh_candles[0]['open'], '  High:', fresh_candles[0]['high'] )
            print('  Low:', fresh_candles[0]['low'], '   Close:', fresh_candles[0]['close'], '  Volume:', fresh_candles[0]['volume'])
            print('\nThe deltas:')
            print('Open:', float(candle[1])-fresh_candles[0]['open'], '  High:', float(candle[2])-fresh_candles[0]['high'])
            print('  Low:', float(candle[3])-fresh_candles[0]['low'], '  Close:', float(candle[4])-fresh_candles[0]['close'], '  Volume:', float(candle[5])-fresh_candles[0]['volume'])
            candle = None
    
    except Exception as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


# if __name__ == '__main__':
    
    