import requests


def getIntruments():
    request = requests.get("http://egchallenge.tech/instruments").json()
    return request

def getCurrentEpoch():
    request = requests.get("http://egchallenge.tech/epoch").json()
    return request['current_epoch']

def getPredictionEpoch():
    request = requests.get("http://egchallenge.tech/epoch").json()
    return request['prediction_epoch']

def getMarketDataIntrument(instrument):
    url = "http://egchallenge.tech"
    request = requests.get("http://egchallenge.t")