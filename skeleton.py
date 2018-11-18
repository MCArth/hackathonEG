import requests
import random
import string
import time

# Very simple example to demonstrate usage of the API.

team_name = 'Keith'
password = 'hunter2'

print(f'team_name = {team_name}')
print(f'password = {password}')

# create_res = requests.post('http://eg
# challenge.tech/team/create', json={'team_name': team_name, 'password': 'password'}).json()
# print(create_res)

login_res = requests.post('http://egchallenge.tech/team/login', json={'team_name': team_name, 'password': password}).json()
print(login_res)

token = login_res['token']
print(f'token = {token}')

last_epoch = None

while True:
    epoch_res = requests.get('http://egchallenge.tech/epoch').json()
    current_epoch = epoch_res['current_epoch']
    prediction_epoch = epoch_res['prediction_epoch']
    timestamp = epoch_res['unix_timestamp']

    print(f'current_epoch = {current_epoch}, prediction_epoch = {prediction_epoch}')

    # We will just submit prediction of -1 * prev return.
    # In a real submission you would probably use a model that you have pre-trained
    # elsewhere.

    marketdata = requests.get('http://egchallenge.tech/marketdata/latest').json()
    predictions = []
    for md in marketdata:
        if md['is_trading']:
            predictions.append({
                'instrument_id': md['instrument_id'],
                'predicted_return': -1.0 * md['epoch_return']
            })
    print(type(predictions))
    print(type(md['instrument_id']))
    print(predictions)
    pred_req = {'token': token, 'epoch': prediction_epoch, 'predictions': predictions}
    print(pred_req)
    pred_res = requests.post('http://egchallenge.tech/predict', json=pred_req)
    print("CUNT " + str(pred_res.status_code))
    print(f'Submitted {len(predictions)} predictions for epoch {prediction_epoch}')

    # Now get our scores for prior predictions
    scores_req = {'token': token}
    scores_res = requests.get('http://egchallenge.tech/scores', json=scores_req).json()
    for score in scores_res:
        epoch = score['epoch']
        pcorr = score['pcorr']
        print(f'epoch = {epoch}, pcorr = {pcorr}')

    next_epoch_in = max(60.0 - (time.time() - timestamp), 0) + 1.0
    print(f'next epoch in {next_epoch_in} sec. Sleeping...')
    time.sleep(next_epoch_in)
