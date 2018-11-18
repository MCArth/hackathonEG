import pandas as pd


def simpMovingAverage(df, n):
    df.rolling(n).mean()

def expWeightFuncs(df, n):
    df.ewm(halflife=n)

#def industryMovingAvg(df, n, industry):

