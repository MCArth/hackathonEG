import getData
import json

def saveData(base, offset, instrumentID):
    data = []
    with open('JsonStore.json', 'w') as f:
        json.dump([], f)

    for i in range(base, base+offset):
        currentEpochDict = getData.getMarketDataEpoch(str(i))
        data.append(currentEpochDict[instrumentID])

    with open('JsonStore.json', 'w') as f:
        json.dump(data, f)
