## Requirements:
* Run main.py to run the program, but first:
* Run "pip install -r requirements.txt" to  install necessary custom packages.
* Create a PostgreSQL database. The code will create two tables in the database: one for storing trade executions and  one for historical candles.
* Also create a database.ini file of the following format or add this section to an existing database.ini file in the folder:
```
[roope_postgresql]
host=localhost
database=markets
user=postgres
password=password
```

## Functionality
The program creates two PostgreSQL tables in a pre-existing database, one for storing trade executions received from FTX's websocket API, and one for storing historical trades from FTX's REST API. Both tables assume multiple exchanges and trade pairs. 
*Note: The trade pair can be changed by editing the necessary variable. However, the endpoints and url paths are currently only configured to work for the FTX exchange.*

The program uses threading to run three processes concurrently:
1. Subscribe to websocket stream and insert trade executions to the 'trade_executions' table.
2. Continuously update most recent candles in the database with trades from trade_executions table.
3. Track the current time and compare the candles in the candles table (constructed from trade executions) to the candles fetched from REST API, for the most recent period. Reports the deltas and open interest at the turn of the period.

Once those three threads have been started, the program fetches 50 candles of historical market data for three intervals, 1 minute, 1 hour, and 1 day, and inserts these candles into the 'candles' table. This number and these intervals can be changed by editing the necessary variables.

## Known Issues
The first candle, (constructed from a partial REST API candle and updated with trades), often has an incorrect volume, and can have an incorrect high and low. This is because the REST API candle is fetched concurrently with the collection of trades, so when the REST API candle arrives before trades start updating, the size of some trades do not get counted in the volume.
* Possible solutions:
    * Ignore first period, and only start updating candles at the turn of the first period after the program is started.
    * Implement a functionality to synchronize the retrieval of the REST API candle with the start of the websocket subscription

FTX has a caching mechanism, which occasionally causes a significant delay in the retrieval of an updated candle. When multiple requests are sent in quick succession, FTX often sends the same, incomplete candle instead of updating it for every request.
* This cache seems to be IP dependent, so it could be circumvented by making requests from multiple IP addresses.

Sometimes, websocket trades are received long after the trade happens, causing delays in updating the most recent candle (the last trades are received up to 10 seconds after the candle has ended).
* This is either an issue with FTX's websocket, or a problem with internet connection.

