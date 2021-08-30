import time
from datetime import datetime
import psycopg2
from config import config
from new_candle import new_candle
from insert import insert_candles

def candle_updater(intervals, exchange, trade_pair):
    """First pulls unprocessed trade executions, updates the appropriate candle,
    and then returns them to the table with processed=True"""
    command_select_trades ="""
    SELECT id,time,price,size FROM trade_executions
    WHERE processed = False AND exchange = %s AND pair = %s
    ORDER BY time ASC;
    """
    command_select_candle = """
    SELECT id,high,low,volume FROM candles
    WHERE exchange = %s AND pair = %s AND interval = %s AND time BETWEEN %s AND %s;
    """
    command_update_candle = """
    UPDATE candles
    SET high = %s, low = %s, volume = %s, close = %s
    WHERE id = %s;
    """
    command_update_trades = """
    UPDATE trade_executions
    SET processed = %s
    WHERE id = %s;
    """
    conn = None
    # connect to database
    params = config()
    conn = psycopg2.connect(**params)
    while True:
        processed_trade_ids = [] 
        for interval in intervals:
            try:
                # create cursor
                cur = conn.cursor()
                # fetch trades that have not been processed, excluding trades that are after the current time interval being processed
                cur.execute(command_select_trades, (exchange, trade_pair))
                
                # look at one trade at a time
                trade_row = cur.fetchone()
                while trade_row is not None:
                    
                    # make sure to only look at the candle in the same time interval as the trade
                    trade_interval_timestamp = datetime.timestamp(trade_row[1])
                    # subtract remainder to round down to interval
                    trade_interval = trade_interval_timestamp - (trade_interval_timestamp % interval)
                    # datetimes that candle will be between:
                    dt1 = datetime.fromtimestamp(trade_interval - 5)
                    dt2 = datetime.fromtimestamp(trade_interval + 5)

                    trade_price = trade_row[2]
                    trade_size = trade_row[3]

                    # new cursor to fetch candle in appropriate interval
                    cur2 = conn.cursor()
                    cur2.execute(command_select_candle, (exchange, trade_pair, interval, dt1, dt2))
                    candle_row = cur2.fetchone()
                    
                    if candle_row == None:
                        # create new candle in this time interval
                        new_candle = [{'time': trade_interval*1000, 'open': trade_price, 'high':trade_price,\
                            'low':trade_price, 'close':trade_price,'volume':trade_size*trade_price}]
                        insert_candles(candles=new_candle,exchange=exchange,pair=trade_pair,interval=interval)

                    else:
                        candle_id = candle_row[0]
                        high = candle_row[1]
                        low = candle_row[2]
                        volume = candle_row[3] + trade_size*trade_price

                        if trade_price > high: # new high
                            high = trade_price 
                        if trade_price < low: # new low
                            low = trade_price
                        close = trade_price # new close

                        # update the candle with these new values
                        cur2.execute(command_update_candle, (high, low, volume, close, candle_id))
                    
                    # log id of trade so it can be updated as processed
                    if trade_row[0] not in processed_trade_ids:
                        processed_trade_ids.append(trade_row[0])

                    conn.commit()

                    cur2.close()

                    # next trade
                    trade_row = cur.fetchone()

            except Exception as error:
                print(error)

        
        for id in processed_trade_ids:
            try:
                cur.execute(command_update_trades, (True, id))
                conn.commit()
                cur.close()
            except Exception as error:
                print(error)



if __name__ == '__main__':
    candle_updater(intervals= [60,60*60,60*60*24], exchange = 'FTX', trade_pair='BTC-PERP')
    