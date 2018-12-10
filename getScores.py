import requests

login_res = requests.post('http://egchallenge.tech/team/login', json={'team_name': 'Keith', 'password': 'hunter2'}).json()
print(login_res)

token = login_res['token']
print(f'token = {token}')
last_scored_epoch = 0

while True:

    scores_req = {'token': token}
    scores_res = requests.get('http://egchallenge.tech/scores', json=scores_req).json()
    for score in scores_res:
        epoch = score['epoch']
        if (epoch > last_scored_epoch):
            last_scored_epoch = epoch
            pcorr = score['pcorr']
            print(f'epoch = {epoch}, pcorr = {pcorr}')
