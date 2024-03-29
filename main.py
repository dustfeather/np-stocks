import argparse
import os
import pandas
import plotly.express as px
import yfinance
from neuralprophet import NeuralProphet

parser = argparse.ArgumentParser("main.py")
parser.add_argument("ticker", help="Ticker", type=str)
args = parser.parse_args()

df = yfinance.download(args.ticker, period='max', interval='1wk').dropna()
df.to_csv('export/data.csv')
df = pandas.read_csv('export/data.csv').rename({'Date': 'ds', 'Adj Close': 'y'}, axis=1)
dfSlim = df.drop('Open', axis=1)
dfSlim = dfSlim.drop('High', axis=1)
dfSlim = dfSlim.drop('Low', axis=1)
dfSlim = dfSlim.drop('Close', axis=1)
dfSlim = dfSlim.drop('Volume', axis=1)
dfSlim = dfSlim[:-1]

model = NeuralProphet(train_speed=-3)
metrics = model.fit(dfSlim, freq="W")
# Export trained model to file
# https://joblib.readthedocs.io/en/latest/generated/joblib.dump.html
future = model.make_future_dataframe(dfSlim, periods=52, n_historic_predictions=len(dfSlim))
forecast = model.predict(future)

fig = px.line(x=forecast['ds'], y=forecast['yhat1'])
fig.add_scatter(x=forecast['ds'], y=dfSlim['y'], mode='lines')

fig.write_json('export/data.json')
