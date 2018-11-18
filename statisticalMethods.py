import pandas as pd
import requests

def simpMovingAverage(df, n):
    return df.rolling(n).mean()

def expWeightFuncs(df, n):
    return df.ewm(halflife=n)

def industryMovingAvg(df, n):
    hot_encoded = pd.get_dummies(df)
    instList = []
    epoch_res = requests.get('http://egchallenge.tech/instruments').json()

    for md in epoch_res:

        instList.append({
            'instrument_id': md['instrument_id'],
            'industry': md['industry'],
            'simpMovingAverage': simpMovingAverage(df, n)
        })

    instList.sort(key=lambda x: x[1])

    industry = instList[0][1]
    industryMovingSum = 0
    i=0

    totalIndustryAvgList = []

    for x in range(len(instList)):
        if instList[x][1] == industry:
            industryMovingSum += instList[x][2]
            i+=1

        else:
            totalIndustryAvgList.append({
                'industry': md['industry'],
                'totalIndustryAvg': industryMovingSum/i
            })

            industry = instList[x][i]
            i=1
            industryMovingSum += instList[x][2]

    return totalIndustryAvgList
