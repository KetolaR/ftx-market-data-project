import psycopg2
from config import config
import datetime

def insert_trade(tradeset):
    """  insert a new trade into the trade_executions table """
    sql = """INSERT INTO trade_executions(time,pair,trade_id,
            price,size,side,liquidation)
            VALUES(%s,%s,%s,%s,%s,%s,%s);"""

    pair = tradeset['market']
    trades = tradeset['data'] # a list of dictionaries
    params = config()
    for trade in trades:
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        try:
            cur.execute(sql,(trade['time'], pair, trade['id'], trade['price'],\
                trade['size'], trade['side'], trade['liquidation']))
            conn.commit()
            cur.close()
        except psycopg2.errors.UniqueViolation as error:
            pass
        except Exception as error:
            print(error)
    conn.close()

def insert_candles(candles, interval = 60, pair = 'BTC-PERP'):
    """ insert a new candle into the candles table,
        given a list of dictionaries in the order: time, pair,
        open, high, low, close, volume, interval"""
    sql = """INSERT INTO candles(time,pair,open,
             high,low,close,volume,interval)
             VALUES(%s,%s,%s,%s,%s,%s,%s,%s);"""

    params = config()
    for candle in candles:
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        try:
            timestamp = datetime.datetime.fromtimestamp(candle['time']/1000)
            cur.execute(sql,(timestamp,pair,candle['open'],candle['high'],\
                candle['low'],candle['close'],candle['volume'],interval))
            conn.commit()
            cur.close()
        except psycopg2.errors.UniqueViolation as error:
            pass
        except Exception as error:
            print(error)
    conn.close()

if __name__ == '__main__':
    import time
    import datetime
    from get_ftx_candles import GetFTXCandles
    
    interval = 60
    x=GetFTXCandles(trade_pair = 'BTC-PERP', candle_resolution = interval, time_length = 240,
        current_time = time.time())
    insert_candles(x.getCandles(), interval = 60, pair = 'BTC-PERP')
