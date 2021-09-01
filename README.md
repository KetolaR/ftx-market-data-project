# In order to run this code, please create a PostgreSQL database. The code will create two tables in the database: one for storing trade executions and  one for historical candles.

# Please also create a database.ini file of the following format or add this section to an existing database.ini file in the folder:
[roope_postgresql]
host=localhost
database=markets
user=postgres
password=password