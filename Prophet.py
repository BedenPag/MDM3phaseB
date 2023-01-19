!pip install prophet

from prophet import Prophet
from prophet.plot import plot_plotly, plot_components_plotly
import pandas as pd

filenamewnhs = '/content/drive/MyDrive/mdmnhs/occwalesnhs.csv'
df = pd.read_csv(filenamewnhs,sep=';')
df
df['cap'] = 100

m = Prophet(growth='logistic')
m.fit(df)
future = m.make_future_dataframe(periods=365)
future['cap'] = 100
forecast = m.predict(future)

fig1 = m.plot(forecast)
fig2 = m.plot_components(forecast)
plot_plotly(m, forecast)
plot_components_plotly(m, forecast)
