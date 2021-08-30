# # time to gaming

# # create SQL tables
# #   - store trade executions (assume multiple trading pairs and exchanges)
# #   - store aggregated historical trade data, "candles"


# # fetch historical data for...
# #   - every minute
# #   - hour
# #   - day

# #   - save that^ data to SQL table #2


# # plug in to websocket
# #   - collect trade executions and store in SQL table #1, creating candles
# #       - minutely, hourly, and daily
# #   - run comparison of created candles to new rest API candles
# #       - log deltas


# # what is open interest?



# # websocket practice

# import websocket




# # sql practice

# import psycopg2
# from config import config

# def connect():
#     """ Connect to the PostgreSQL database server"""
#     conn = None
#     try:
#         # read connection paramaters
#         params = config() 

#         # connect to PostgreSQL server
#         print('Connecting to the PostgreSQL database...')
#         conn = psycopg2.connect(**params)

#         # create a cursor
#         cur = conn.cursor()

#         # execute a statement
#         print('PostgreSQL database version:')
#         cur.execute('SELECT version()')

#         # display the PostgreSQL database server version
#         db_version = cur.fetchone()
#         print(db_version)

#         # close communication with PostgreSQL
#         cur.close()
    
#     except Exception as error:
#         print(error)
#     finally:
#         if conn is not None:
#             conn.close()
#             print('Database connection closed.')

# if __name__ == '__main__':
#     # def inserter():
#     #     "Takes in list of dictionaries, iterates thru and inserts into sql table"
#     # import time
#     # import datetime
#     # params =  {
#     #     "market_name": 'BTC-PERP',
#     #     "resolution": 60,
#     #     "start_time": time.time()-240,
#     #     "end_time": time.time(),
#     #     "limit": 5000
#     # }
#     # response = requests.get('https://ftx.com/api/markets/)

#     #detect the turn of a period
#     from datetime import datetime
#     import time
#     # chef = datetime.fromtimestamp(1630179840000.0/1000)
#     # print(chef)
#     # b0ss = datetime.timestamp(chef)
#     # print(b0ss)

#     min = 60
#     hour = 60*min
#     day = 24*hour
#     timestamp = 1630179840
#     counter = time.time()

#     dt = datetime.fromtimestamp(timestamp)
#     print(dt.minute)

# THREADING PRACTICE

# from threading import Thread
# import time

# def method1():
#     print('i am method 1')
#     time.sleep(1)
#     print('method1 done')


# def method2():
#     print('i am method 2')
#     time.sleep(1)
#     print('method2 done')

# def method3():
#     print('method3 start')
#     print('method3 start')    
#     time.sleep(10)
#     print('method3 end ')

# def main():
#     event_q = [3,1,2,2,1,2,1,1,1,1]
#     print(f'Event order --{event_q}')
#     ls = []
#     for e in event_q:
#         print(f'event {e}')
#         if e == 1:
#             m = method1
#         elif e == 3:
#             m = method3
#         else:
#             m = method2
#         t = Thread(target=m)
#         ls.append(t)
#         t.start()
#     print('done')

# main()
# print('AFTER MAIN')



import time
from datetime import datetime
start_time = time.time() # record the start-time of retrieving trade info
current_time_interval = start_time - (start_time % 60)
print(datetime.fromtimestamp)

# current_dt = datetime.datetime.fromtimestamp(current_time_interval)
# print(current_dt)


# def recent_candles():
#     for interval in intervals:
#         window = interval * 4 
#         fresh_candles = FTXCandles(trade_pair = trade_pair, candle_resolution = interval,
#                                 history_length=window, current_time = time.time())
#         insert_candles(fresh_candles.get_candles(), exchange = 'FTX', interval = interval, pair = trade_pair)

# timy = datetime.datetime.fromtimestamp(time.time())
# bruh = 650
# jimbo = 340
# print('time:', timy, 'bruh:', bruh)

# import time
# from datetime import datetime
# from ftx_candles import FTXCandles
# start_time = time.time()
# current_interval_timestamp = start_time - (start_time % 60) # current time rounded down to nearest minute
# current_interval_dt = datetime.fromtimestamp(current_interval_timestamp)
# interval = 60
# window = interval*2
# fresh_candles = FTXCandles(trade_pair = 'BTC-PERP', candle_resolution = interval,
#                         history_length=window, current_time = start_time)
# x = fresh_candles.get_candles()
# print(datetime.fromtimestamp(x[0]['time']/1000))
# print(datetime.fromtimestamp(x[1]['time']/1000))
# print(current_interval_dt)


