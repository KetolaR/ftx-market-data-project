#######################################
# Coding Project for TradeBlock
# Roope Ketola
# 08/31/2021
#######################################

# import necessary modules
from update_candle import update_candle
from create_table import create_tables
from ftx_candles import FTXCandles
from insert import insert_candles
from ftx_websocket import FTXWebsocket
from compare_candles import compare_candles 
import time
from datetime import datetime
from threading import Thread


# necessary variables
intervals = [60, 60*60, 60*60*24]
trade_pair = 'BTC-PERP'
exchange = 'FTX'

# define necessary methods not imported:
    # For continous processes, we need a way to track the current interval/period.
    # At the turn of the period, compare most recent candle from REST API candle to candle constructed from websocket trades
def timer():
    while True:
        current_time = time.time()
        # current minute interval:
        current_interval_timestamp = current_time - ( current_time % 60)
        # compare candles for this past minute:
        print('The minute changed. Comparing candles...')
        compare_candles(interval=60,current_interval_timestamp=current_interval_timestamp,exchange=exchange,trade_pair=trade_pair)

        # if the hour also changed:
        if datetime.fromtimestamp(current_interval_timestamp).hour > datetime.fromtimestamp(current_interval_timestamp-60).hour or\
            datetime.fromtimestamp(current_interval_timestamp).day > datetime.fromtimestamp(current_interval_timestamp-60).day:
            # compare candles for this past hour:
            print('The hour changed. Comparing candles...')
            compare_candles(interval=60*60,current_interval_timestamp=current_interval_timestamp,exchange=exchange,trade_pair=trade_pair)

        # if the day also changed:
        if datetime.fromtimestamp(current_interval_timestamp).day > datetime.fromtimestamp(current_interval_timestamp-60).day or\
            datetime.fromtimestamp(current_interval_timestamp).month > datetime.fromtimestamp(current_interval_timestamp-60).month:
            # compare candles for this past day:
            print('The day changed. Comparing candles...')
            compare_candles(interval=60*60*24,current_interval_timestamp=current_interval_timestamp,exchange=exchange,trade_pair=trade_pair)
            
        # wait until the next call should happen
        next_call = current_interval_timestamp + 60
        time.sleep(next_call - time.time())



# Create SQL tables to store data: trade executions and historical candles
create_tables()


# Subscribe to FTX's Websocket stream
#   - use threading with other continuous processes
t1 = Thread(target = FTXWebsocket().subscribe) # the subscribe method automatically inserts
t1.start()                                        # into the PostgreSQL table
time.sleep(10) # allow time for websocket to connect


# update most recent candles with trade executions
t2 = Thread(target=update_candle, kwargs={'intervals': intervals, 'exchange': exchange, 'trade_pair': trade_pair})
t2.start()

# record the start-time of retrieving trade info
start_time = time.time()
start_datetime = datetime.fromtimestamp(start_time) 
current_interval_timestamp = start_time - (start_time % 60) # current time rounded down to nearest minute
current_interval_dt = datetime.fromtimestamp(current_interval_timestamp)
print('\nStarting time interval:',current_interval_dt, '\n')


# start the timers, and period-dependent methods
t3 = Thread(target=timer)
t3.start()

# Fetch historical data: 1 minute, 1 hour, and 1 day candles from FTX's REST API
print('Fetching historical data from REST API... \n')
for interval in intervals:
    window = interval * 50 # get last 50 candles for each interval
    ftx_candles = FTXCandles(trade_pair = trade_pair, candle_resolution = interval,
                            history_length=window, current_time = start_time)

    # Save historical data to SQL tables
    insert_candles(ftx_candles.get_candles(), exchange = exchange, interval = interval, pair = trade_pair)




# Record open interest at close of each interval