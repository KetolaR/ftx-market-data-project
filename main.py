#######################################
# Coding Project for TradeBlock
# Roope Ketola
# 08/30/2021
#######################################

# import necessary modules
from new_candle import new_candle
from candle_updater import candle_updater
from create_table import create_tables
from ftx_candles import FTXCandles
from insert import insert_candles, insert_trade
from ftx_websocket import FTXWebsocket
from compare_candles import compare_candles 
from config import config
import psycopg2
import time
from datetime import datetime
from threading import Thread


# define necessary methods not imported

# For continous processes, we need a way to track the current interval/period.
# At the turn of the period, compare most recent candle from REST API candle to candle constructed from websocket trades
# def timer():
#     while True:
#         current_time = time.time()
#         current_interval_timestamp = current_time - ( current_time % 60)
#         current_interval_dt = datetime.fromtimestamp(current_interval_timestamp)
#         current_dt = datetime.fromtimestamp(time.time())
#         if current_dt.minute > current_interval_dt.minute or current_dt.hour > current_interval_dt.hour:
#             current_interval_timestamp = current_interval_timestamp + 60
#             print('minute changed, checking most recent minute-candle.')
#             print('current time interval is now:', datetime.fromtimestamp(current_interval_timestamp))
#             compare_candles(interval=60, current_interval_timestamp=current_interval_timestamp, exchange=exchange, trade_pair=trade_pair)
#             if current_dt.hour > current_interval_dt.hour or current_dt.day > current_interval_dt.day:
#                 print('hour changed, checking most recent hour-candle\n')
#                 compare_candles(interval=60*60, current_interval_timestamp=current_interval_timestamp, exchange=exchange, trade_pair=trade_pair)
#                 if current_dt.day > current_interval_dt.day or current_dt.month > current_interval_dt.month:
#                     print('day changed, checking most recent day-candle\n')
#                     compare_candles(interval=60*60*24, current_interval_timestamp=current_interval_timestamp, exchange=exchange, trade_pair=trade_pair)


# necessary variables
intervals = [60, 60*60, 60*60*24]
trade_pair = 'BTC-PERP'
exchange = 'FTX'


def timer():
    while True:
        current_time = time.time()
        current_interval_timestamp = current_time - ( current_time % 60)
        compare_candles(interval=60,current_interval_timestamp=current_interval_timestamp,exchange=exchange,trade_pair=trade_pair)
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
# t2 = Thread(target=candle_updater, kwargs={'intervals': intervals, 'exchange': exchange, 'trade_pair': trade_pair})
# t2.start()

# record the start-time of retrieving trade info
start_time = time.time()
start_datetime = datetime.fromtimestamp(start_time) 
current_interval_timestamp = start_time - (start_time % 60) # current time rounded down to nearest minute
current_interval_dt = datetime.fromtimestamp(current_interval_timestamp)
print('\nStarting time interval:',current_interval_dt, '\n')


# start the timer, and period-dependent methods
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