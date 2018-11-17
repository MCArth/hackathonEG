import getData
import numpy as np
import statsmodels.api as sm


#print(getData.getMarketDataIntrument("1"))
# for inst in getInstruments:

Y = []

marketData1 = getData.getMarketDataIntrument("1")

for epoch in marketData1:
    #list1.append({
    #    'epoch': epoch['epoch'],
    #    'epoch_return': epoch['epoch_return']
    #})

    Y.append(epoch["epoch_return"])

print(Y)