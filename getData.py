import requests

#ALL RETURNED AS JSON

#returns JSON list of instruments
def getIntruments():
    request = requests.get("http://egchallenge.tech/instruments").json()
    return request

#returns current epoch
def getCurrentEpoch():
    request = requests.get("http://egchallenge.tech/epoch").json()
    return request['current_epoch']

#returns prediction epoch
def getPredictionEpoch():
    request = requests.get("http://egchallenge.tech/epoch").json()
    return request['prediction_epoch']

#returns market data for specific instrument
def getMarketDataIntrument(instrument):
    url = "http://egchallenge.tech/marketdata/instrument/" + instrument
    return requests.get(url).json()

#returns market data for given epoch
def getMarketDataEpoch(epoch):
    url = "http://egchallenge.tech/marketdata/epoch/" + epoch
    return requests.get(url).json()

#returns latest market data
def getMarketDataLatest():
    return requests.get("http://egchallenge.tech/marketdata/latest").json()

