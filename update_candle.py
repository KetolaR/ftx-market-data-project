from datetime import datetime
import psycopg2
from config import config
from insert import insert_candles


def update_candle(exchange, trade_pair, intervals):
    """Fetch unprocessed trades from trade_executions table,
        use each one to update the appropriate candle in the candles table,
        return the trades to the trade_executions table with processed=true."""

    sql_fetch_trades = """
    SELECT id,time,price,size FROM trade_executions
    WHERE processed=false AND exchange=%s AND pair=%s
    ORDER BY time ASC;
    """

    sql_fetch_candle = """
    SELECT id,high,low,close,volume FROM candles
    WHERE exchange=%s AND pair=%s AND interval=%s AND time=%s;
    """

    sql_return_candle = """
    UPDATE candles
    SET high=%s, low=%s, close=%s, volume=%s
    WHERE id=%s;
    """

    sql_return_trade = """
    UPDATE trade_executions
    SET processed=true
    WHERE id=%s;
    """

    # connect to database
    params = config()
    conn = psycopg2.connect(**params)

    # create cursors
    cur1 = conn.cursor()
    cur2 = conn.cursor()

    while True:
        trade_ids = [] # a list of ids for trades that have been processed

        # fetch trades
        cur1.execute(sql_fetch_trades, (exchange, trade_pair))
        trade_row = cur1.fetchone()
    

        # loop until fetch runs out of trades
        while trade_row is not None:

            # each trade should be included in each interval's candle
            for interval in intervals:

                # record the information of the trade
                trade_info = {'id':trade_row[0], 'time':trade_row[1], 'price':trade_row[2], 'size':trade_row[3]}

                # locate the datetime of the appropriate candle
                # round down the trade's timestamp to the appropriate interval
                ts = datetime.timestamp(trade_info['time'])
                ts = ts - (ts % interval)

                # grab the candle whose time corresponds to that interval
                cur2 = conn.cursor() # another cursor for fetching candles
                cur2.execute(sql_fetch_candle, (exchange,trade_pair,interval,datetime.fromtimestamp(ts)))
                candle = cur2.fetchone()
                
                if candle is not None:
                    # if candle exists, compare trade values to candle
                    candle_info = {'id':candle[0], 'high':candle[1], 'low':candle[2], 'close':candle[3],'volume':candle[4]}

                    if trade_info['price'] > candle_info['high']:
                        candle_info['high'] = trade_info['price']
                    if trade_info['price'] < candle_info['low']:
                        candle_info['low'] = trade_info['price']

                    candle_info['volume'] = candle_info['volume'] + (trade_info['price']*trade_info['size'])
                    candle_info['close'] = trade_info['price']

                    # update the candle with the new values
                    cur2.execute(sql_return_candle, (candle_info['high'], candle_info['low'], candle_info['close'], candle_info['volume'], candle_info['id']))

                else: # if candle does not exist, add a candle
                    new_candle = [{'time':ts*1000, 'open':trade_info['price'], 'high':trade_info['price'],\
                        'low':trade_info['price'], 'close':trade_info['price'], 'volume':trade_info['price']*trade_info['size']}]
                    insert_candles(candles=new_candle, exchange=exchange, pair=trade_pair, interval=interval)
                
            # trade inserted into candles for all intervals...
            # mark trade as processed
            trade_ids.append(trade_info['id'])

            # new trade
            trade_row = cur1.fetchone()

        # last trade fetch was empty, return processed trades
        for trade_id in trade_ids:
            cur2.execute(sql_return_trade, (trade_id,))
            
        conn.commit()

        # loop again: pull new trades
        

if __name__ == '__main__':
    update_candle(exchange='FTX',trade_pair='BTC-PERP',intervals=[60,60*60,60*60*24])
