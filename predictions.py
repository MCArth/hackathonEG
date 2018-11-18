import requests
import json

#Takes token and predictions and generates and sends JSON
#Returns status code
def sendPredictions(predictions, predictionEpoc):
    payload = {
        'token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0aWQiOjE0fQ.giHEykztGqIO988hG5jr468vWo3yE2c4OTFT6MAzqqk',
        'epoch': predictionEpoc,
        'predictions': predictions
    }
    with open('sentData.json', 'w') as f:
        json.dump(payload, f)

    req = requests.post('http://egchallenge.tech/predict', json=payload)
    return req.status_code

def getPastPreciction(epoch):
        payload = {
            'token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0aWQiOjE0fQ.giHEykztGqIO988hG5jr468vWo3yE2c4OTFT6MAzqqk',
            'epoch': epoch
        }
        return requests.get("http://egchallenge.tech.predict", json=payload).json()