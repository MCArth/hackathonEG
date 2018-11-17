#import pandas
import getData
import json

def saveData():
    with open('JsonStore.json', 'w') as f:
        json.dump([], f)

    data = []
    for i in range(baseEpoch, getData.getCurrentEpoch()+1):
        currentEpochDict = getData.getMarketDataEpoch(str(i))
        data.append(currentEpochDict)

    with open('JsonStore.json', 'w') as f:
        json.dump(data, f)


baseEpoch = 3000

saveData()

