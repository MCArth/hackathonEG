import getData
import numpy as np
import statsmodels.api as sm


#print(getData.getMarketDataIntrument("1"))
# for inst in getInstruments:

Y = []
X = []

marketData1 = getData.getMarketDataIntrument("1")


for epoch in marketData1:
    #list1.append({
    #    'epoch': epoch['epoch'],
    #    'epoch_return': epoch['epoch_return']
    #})
    X.append(epoch["epoch"])
    Y.append(epoch["epoch_return"])


Y.pop(0)

X.pop(0)

X = sm.add_constant(X)
model = sm.OLS(Y, X)
results = model.fit()
#results.params
#results.tvalues
print(results.t_test([1, 0]))
print(results.f_test(np.identity(2)))

print(X)
print(Y)