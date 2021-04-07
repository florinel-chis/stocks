import json
import pandas
import sys

filename =  'spy-1w.json'
with open(filename,'r') as f:
    spy = json.load(f)

df = pandas.DataFrame(data=spy['Candles'][0]['Candles'])
df['date'] = pandas.to_datetime(df['FromDate'], infer_datetime_format=True)
#df = df[df['date']<'2020-03-01']
k=0
buyPrice=[]
df['buy'] = df.index % 4
df['buyPrice'] = (df['Low']+df['High'])/2
df['positions'] = 500/df['buyPrice']
df['investedAmount'] = 500


print(df.head())
dfBought = df[df['buy']==0]
print(dfBought)
boughtPositions = dfBought['positions'].sum()

print("numar pozitii:",boughtPositions," pret mediu: ",dfBought['buyPrice'].mean())
print("Suma investita: {:.2f}".format(dfBought['investedAmount'].sum()))
lastPrice = df.iloc[-1]['Close']
print("Pret curent: ",lastPrice)
potentialProfit = boughtPositions*lastPrice-dfBought['buyPrice'].sum()
print("Profit potential: ", boughtPositions*lastPrice,"-",dfBought['buyPrice'].sum(),"=",potentialProfit)

filename =  'spy-dividends.tsv'
dividends = pandas.read_csv(filename,"\t")
dividends['date'] = pandas.to_datetime(dividends['eff_date'])
totalDividends = 0
for idx,div in dividends.iterrows():
    subset = dfBought[dfBought['date'] < div['date']]
    positionsForDividends = subset['positions'].sum()
    divAmount = positionsForDividends*div['amount'] / 1.3
    totalDividends += divAmount
    print("Dividende la data ",div['date'],'=',divAmount)

print("Total: ",totalDividends)