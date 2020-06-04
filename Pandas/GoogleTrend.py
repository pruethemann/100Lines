from pytrends.request import TrendReq
import matplotlib.pyplot as plt

from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

## Verbinde zu Google Trend
pytrends = TrendReq(hl='en-US', tz=360)

## Definiere gewünschte Keywords als Liste
keywords = ["Ski", 'Snow', 'Flu']

## Rufe die Trends in einem gewünschten Zeitinterval ab. Geo begrenzt das Land
pytrends.build_payload(keywords, cat=0, timeframe = '2010-01-01 2019-10-01', geo='', gprop='')
trend_df = pytrends.interest_over_time()

## Impression der Daten
print(trend_df.head())

## Nutze den Index (Daten) als eigene Column
trend_df['date'] = trend_df.index

## Erstelle mehrere "Linien" in einem Plot
_, ax = plt.subplots()

## Plotte jedes Keyword einzeln
for keyword in keywords:
    trend_df.plot(x='date', y=keyword, ax=ax)

## Plotte die Trends und den Graphen
plt.title("Google Trends")
plt.legend()
plt.show()

trend_df.pct_change()
