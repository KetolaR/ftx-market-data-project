# time to gaming

# create SQL tables
#   - store trade executions (assume multiple trading pairs and exchanges)
#   - store aggregated historical trade data, "candles"


# fetch historical data for...
#   - every minute
#   - hour
#   - day

#   - save that^ data to SQL table #2


# plug in to websocket
#   - collect trade executions and store in SQL table #1, creating candles
#       - minutely, hourly, and daily
#   - run comparison of created candles to new rest API candles
#       - log deltas


# what is open interest?



# websocket practice

import websocket




# sql practice

import psycopg2
from config import config

def connect():
    """ Connect to the PostgreSQL database server"""
    conn = None
    try:
        # read connection paramaters
        params = config() 

        # connect to PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)

        # create a cursor
        cur = conn.cursor()

        # execute a statement
        print('PostgreSQL database version:')
        cur.execute('SELECT version()')

        # display the PostgreSQL database server version
        db_version = cur.fetchone()
        print(db_version)

        # close communication with PostgreSQL
        cur.close()
    
    except Exception as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')

if __name__ == '__main__':
    # def inserter():
    #     "Takes in list of dictionaries, iterates thru and inserts into sql table"
    # import time
    # import datetime
    # params =  {
    #     "market_name": 'BTC-PERP',
    #     "resolution": 60,
    #     "start_time": time.time()-240,
    #     "end_time": time.time(),
    #     "limit": 5000
    # }
    # response = requests.get('https://ftx.com/api/markets/)