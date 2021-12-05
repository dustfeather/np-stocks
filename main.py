from neuralprophet import NeuralProphet
import pandas as pd
import yfinance as yf
import plotly.express as px
import argparse
import os

parser = argparse.ArgumentParser("main.py")
parser.add_argument("ticker", help="Ticker", type=str)
args = parser.parse_args()

df = yf.download(args.ticker, period='max', interval='1d')
df.to_csv('export/data.csv')
df = pd.read_csv('export/data.csv').rename({'Date': 'ds', 'Adj Close': 'y'}, axis=1)
dfSlim = df.drop('Open', axis=1)
dfSlim = dfSlim.drop('High', axis=1)
dfSlim = dfSlim.drop('Low', axis=1)
dfSlim = dfSlim.drop('Close', axis=1)
dfSlim = dfSlim.drop('Volume', axis=1)

model = NeuralProphet(daily_seasonality=True, yearly_seasonality=True, weekly_seasonality=True, epochs=500)
metrics = model.fit(dfSlim, freq="D")
future = model.make_future_dataframe(dfSlim, periods=365, n_historic_predictions=len(dfSlim))
forecast = model.predict(future)

fig = px.line(x=forecast['ds'], y=forecast['yhat1'])
fig.add_candlestick(x=forecast['ds'], open=df['Open'], close=df['y'], high=df['High'], low=df['Low'])

fig.write_json('export/data.json')
os.remove('export/data.csv')
