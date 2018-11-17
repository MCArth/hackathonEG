import pandas as pd

import requests
import pickle
import time
import getData

def get_returns(t):
    r = requests.get("http://egchallenge.tech/marketdata/epoch/" + str(t))
    # The data is formatted as a list of dictionaries
    # We pass it to the DataFrame constructor to create a DataFrame,
    # then select the epoch_return column (returned as a Pandas Series)
    return pd.DataFrame(r.json())["epoch_return"]


def save_returns_df(df_to_save):
    with open("example_returns_df", "wb") as f:
        # pickle.dump saves a python object to a file,
        # in a way which can be later restored with pickle.load
        pickle.dump(df_to_save, f)


def create_returns_df(target_epoch=3000):
    try:
        with open("example_returns_df", "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        # This will happen the first time we run the program,
        # because the file won't exist yet
        # So we have to download the data and put it in a DataFrame
        ret = {}
        for t in range(target_epoch):
            if (t % 20 == 0):
                print("Downloading returns for epoch " + str(t))
            ret[t] = get_returns(t)
        # When fed a dictionary { colname_i : column_i },
        # the DataFrame constructer will create columns
        # with name colname_i and data column_i
        ret = pd.DataFrame(ret)
        save_returns_df(ret)
        return ret

def update_returns_df(input_df, target_epoch=None):
    current_epoch = requests.get('http://egchallenge.tech/epoch').json()['current_epoch']
    print("Current epoch:", current_epoch)

    # If target_epoch is None then we want to bring the dataframe fully up-to-date
    if target_epoch is None or current_epoch < target_epoch:
        last_epoch_to_get = current_epoch
    else:
        last_epoch_to_get = target_epoch

    last_downloaded_epoch = max(input_df.columns)

    while last_downloaded_epoch < last_epoch_to_get:
        print("Downloading returns up to epoch ", last_epoch_to_get)

        for t in range(last_downloaded_epoch + 1, last_epoch_to_get + 1):
            if (t % 20 == 0):
                print("Downloading returns for epoch ", t)
            input_df[t] = get_returns(t)

        # If we had to make a large update, it's possible that the epoch advanced
        # in the meantime
        # In this case we may want to download the returns for the new epochs as well
        last_downloaded_epoch = last_epoch_to_get

        current_epoch = requests.get('http://egchallenge.tech/epoch').json()['current_epoch']
        print("Current epoch:", current_epoch)
        if target_epoch is None or current_epoch < target_epoch:
            last_epoch_to_get = current_epoch

    # Save the results so we don't have to re-download them next time
    save_returns_df(input_df)

    timestamp = requests.get('http://egchallenge.tech/epoch').json()['unix_timestamp']
    next_epoch_in = max(60.0 - (time.time() - timestamp), 0) + 1.0
    return next_epoch_in

df = create_returns_df()

while(True):
    update_returns_df(df)
    startEpoc = getData.getCurrentEpoch()
    while (startEpoc == getData.getCurrentEpoch()):
        a = 1+1