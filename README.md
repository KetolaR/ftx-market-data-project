# In order to run this code, please create a PostgreSQL database for use by this code. The code will create two tables in the database, for storing trade executions and historical candles.

# Please also create a database.ini file of the following format or add this section to an existing database.ini file:
[postgresql]
host=localhost
database=markets
user=postgres
password=password