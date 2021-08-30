import psycopg2
from config import config
import datetime

def insert_trade(tradeset, exchange, processed, time_received):
    """  insert a new trade into the trade_executions table """
    sql = """INSERT INTO trade_executions(time,exchange,pair,trade_id,
            price,size,side,liquidation,processed,time_received)
            VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            ON CONFLICT (trade_id, exchange, pair)
            DO UPDATE SET processed = EXCLUDED.processed;"""

    pair = tradeset['market']
    trades = tradeset['data'] # a list of dictionaries
    params = config()
    for trade in trades:
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        try:
            cur.execute(sql,(trade['time'], exchange, pair, trade['id'], trade['price'],\
                trade['size'], trade['side'], trade['liquidation'], processed,time_received))
            conn.commit()
            cur.close()
        except psycopg2.errors.UniqueViolation as error:
            print(error)
        except Exception as error:
            print(error)
    conn.close()


def insert_candles(candles, exchange, pair, interval):
    """ insert a new candle into the candles table,
        given a list of dictionaries in the order: time, exchange,
        pair, open, high, low, close, volume, interval"""
    sql = """INSERT INTO candles(time,exchange,pair,open,
             high,low,close,volume,interval)
             VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)
             ON CONFLICT (time,exchange,pair,interval)
             DO UPDATE SET open = EXCLUDED.open, high = EXCLUDED.high,
             low = EXCLUDED.low, close = EXCLUDED.close, volume = EXCLUDED.volume;"""

    params = config()
    for candle in candles:
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        try:
            timestamp = datetime.datetime.fromtimestamp(candle['time']/1000)
            cur.execute(sql,(timestamp,exchange,pair,candle['open'],candle['high'],\
                candle['low'],candle['close'],candle['volume'],interval))
            conn.commit()
            cur.close()
        except psycopg2.errors.UniqueViolation as error:
            print(error)
        except Exception as error:
            print(error)
    conn.close()

if __name__ == '__main__':
    import time
    import datetime
    from ftx_candles import FTXCandles
    
    interval = 60
    x=FTXCandles(trade_pair = 'BTC-PERP', candle_resolution = interval, time_length = 240,
        current_time = time.time())
    print(x.get_candles())
    insert_candles(x.get_candles(), interval = 60, pair = 'BTC-PERP')
