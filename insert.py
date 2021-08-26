import psycopg2
from config import config

def insert_trade():
    """  insert a new trade into the trade_executions table """
    sql = """INSERT INTO trade_executions(time,trade_id,pair,price,size,side,liquidation)"""
def insert_candle(candles):
    """ insert a new candle into the candles table,
        given a list of sets in the order: time, pair,
        open, high, low, close, volume, interval"""
    sql = """INSERT INTO candles(time,pair,open,
             high,low,close,volume,interval)
             VALUES(%s,%s,%s,%s,%s,%s,%s,%s);"""
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        for candle in candles:
            cur.execute(sql,candle)
        conn.commit()
        cur.close()
    except Exception as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

if __name__ == '__main__':
    import time
    import datetime
    ls = []
    ls.append((datetime.datetime.fromtimestamp(time.time()), 'BTC-PERP', 59.25,189.0,143.5,155.25,193.95725,600))
    time.sleep(1)
    ls.append((datetime.datetime.fromtimestamp(time.time()), 'BTC-PERP', 11059.25,11089.0,11043.5,11055.25,464193.95725,60))
    insert_candle(ls)

