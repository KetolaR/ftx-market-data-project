import requests
import json
import time

def ftx_open_interest(pair):

    endpoint = f'https://ftx.com/api/futures/{pair}'
    response = requests.get(endpoint).json()
    if response['success'] == False:
        print("Error occured during open_interest 'get' request")
    
    response = response['result']
    open_interest_usd = response['openInterestUsd']
    open_interest = response['openInterest']
    print('Currently,\nOpen Interest (in number of contracts):\n', open_interest)
    print('Open Interest (in USD):\n', open_interest_usd)



if __name__ == "__main__":
    ftx_open_interest(pair = 'BTC-PERP')