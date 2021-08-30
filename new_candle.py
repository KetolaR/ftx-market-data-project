from insert import insert_candles
import psycopg2
from config import config
from datetime import datetime
import time


def new_candle(interval,current_interval_timestamp, exchange, trade_pair, price):
    """Insert a new candle into the candles database using the first trade in this time period."""
    command = """
    SELECT price FROM trade_executions
    WHERE time > %s
    ORDER BY time ASC
    LIMIT 1;"""
    
    conn = None
    price = None
    while price == None:
        try:
            params = config()
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            cur.execute(command, (datetime.fromtimestamp(current_interval_timestamp),))
            price = cur.fetchone()

            if price is not None:
                # create a correctly formatted candle
                new_candle = [{'time': current_interval_timestamp*1000, 'open': price[0], 'high':price[0],\
                    'low':price[0], 'close':price[0],'volume':0}] # volume=0 because the size of this trade will be added to volume later
                insert_candles(candles=new_candle,exchange=exchange,pair=trade_pair,interval=interval)
                conn.commit()
                print("Created a new candle for this time interval.")
            cur.close()
            
        except Exception as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
                time.sleep(2)
