import requests


#returns instruments JSON
def getIntruments():
    request = requests.get("http://egchallenge.tech/instruments").json()
    return request

#returns current epoch INT
def getCurrentEpoch():
    request = requests.get("http://egchallenge.tech/epoch").json()
    return request['current_epoch']

#returns prediction epoch INT
def getPredictionEpoch():
    request = requests.get("http://egchallenge.tech/epoch").json()
    return request['prediction_epoch']

#returns market data for specific instrument JSON
def getMarketDataIntrument(instrument):
    url = "http://egchallenge.tech/marketdata/instrument/" + instrument
    return requests.get(url).json()

#returns market data for given epoch JSON
def getMarketDataEpoch(epoch):
    url = "http://egchallenge.tech/marketdata/epoch/" + epoch
    return requests.get(url).json()

#returns latest market data JSON
def getMarketDataLatest():
    return requests.get("http://egchallenge.tech/marketdata/latest").json()

