import requests
import getData
import numpy as np

#Takes token and predictions and generates and sends JSON
#Returns status code
def sendPredictions(predictions):
    payload = {
        'token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0aWQiOjE0fQ.giHEykztGqIO988hG5jr468vWo3yE2c4OTFT6MAzqqk',
        'epoch': getData.getPredictionEpoch(),
        'predictions': predictions
    }
    req = requests.post("http://egchallenge.tech/predict", json=payload)
    return req.status_code

def getPastPreciction(epoch):
        payload = {
            'token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0aWQiOjE0fQ.giHEykztGqIO988hG5jr468vWo3yE2c4OTFT6MAzqqk',
            'epoch': epoch
        }
        return requests.get("http://egchallenge.tech.predict", json=payload).json()