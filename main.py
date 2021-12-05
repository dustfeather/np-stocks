from neuralprophet import NeuralProphet
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import argparse

mpl.rcParams['figure.dpi'] = 150
savefig_options = dict(format="png", bbox_inches="tight")

parser = argparse.ArgumentParser("main.py")
parser.add_argument("url", help="Yahoo finance CSV download url", type=str)
args = parser.parse_args()

df = pd.read_csv(args.url).rename({'Date': 'ds', 'Adj Close': 'y'}, axis=1)
df = df.drop('Open', axis=1)
df = df.drop('High', axis=1)
df = df.drop('Low', axis=1)
df = df.drop('Close', axis=1)
df = df.drop('Volume', axis=1)
df = df.drop(len(df) - 1, axis=0)

model = NeuralProphet(epochs=500)
metrics = model.fit(df, freq="MS")
future = model.make_future_dataframe(df, periods=12, n_historic_predictions=len(df))
forecast = model.predict(future)

fig, ax = plt.subplots(figsize=(14, 10))
model.plot(forecast, xlabel="Date", ylabel="Close", ax=ax)
ax.xaxis.label.set_size(28)
ax.yaxis.label.set_size(28)
ax.tick_params(axis='both', which='major', labelsize=24)
ax.set_title("1Y Price prediction", fontsize=28, fontweight="bold")

fig.savefig("images/forecast.png", **savefig_options)
# fig_param = model.plot_parameters()
# fig_param.savefig("params.png", **savefig_options)
