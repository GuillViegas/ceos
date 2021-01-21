from bitcoin import BitcoinTimeSeries
from datetime import datetime
from indicators import ema, rsi, bb


btc = BitcoinTimeSeries(path='bitstampUSD_1-min_data_2012-01-01_to_2020-12-31.csv')

ema = btc.result_set('2020-01-01 00:00:00', '2020-12-30 23:55:00', 'Close', ema)
rsi = btc.result_set('2020-01-01 00:00:00', '2020-12-30 23:55:00', 'Close', rsi)
sma, down_bb, up_bb = btc.result_set('2020-01-01 00:00:00', '2020-12-30 23:55:00', 'Close', bb)

df = ema.to_frame(name='ema').join(rsi.to_frame(name='rsi')).join(sma.to_frame(name='sma')).join(down_bb.to_frame(name='down_bb')).join(up_bb.to_frame(name='up_bb'))
df['Timestamp'] = df.index
df['Timestamp'] = df['Timestamp'].apply(datetime.timestamp)

df.to_csv('btc_indicators.csv', index=False)