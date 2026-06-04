import requests
import pandas as pd

def get_binance_ohlcv(symbol, start_str, end_str, interval='1d'):
    url = "https://api.binance.com/api/v3/klines"
    start_ts = int(pd.Timestamp(start_str, tz='UTC').timestamp() * 1000)
    end_ts   = int(pd.Timestamp(end_str,   tz='UTC').timestamp() * 1000)
    
    all_data = []
    while start_ts < end_ts:
        params = {
            'symbol': symbol,
            'interval': interval,
            'startTime': start_ts,
            'endTime': end_ts,
            'limit': 1000
        }
        resp = requests.get(url, params=params).json()
        if not resp:
            break
        all_data.extend(resp)
        start_ts = resp[-1][0] + 1
    
    df = pd.DataFrame(all_data, columns=[
        'open_time','open','high','low','close','volume',
        'close_time','quote_volume','trades',
        'taker_buy_base','taker_buy_quote','ignore'
    ])
    df['Date'] = pd.to_datetime(df['open_time'], unit='ms', utc=True).dt.normalize()
    df['open']   = df['open'].astype(float)
    df['high']   = df['high'].astype(float)
    df['low']    = df['low'].astype(float)
    df['close']  = df['close'].astype(float)
    df['volume'] = df['volume'].astype(float)
    return df[['Date', 'open', 'high', 'low', 'close', 'volume']].copy()

# Tarik data
btc_price = get_binance_ohlcv('BTCUSDT', '2020-10-01', '2026-03-20')
eth_price = get_binance_ohlcv('ETHUSDT', '2020-10-01', '2026-03-20')
sol_price = get_binance_ohlcv('SOLUSDT', '2020-10-01', '2026-03-20')

# Simpan ke CSV
btc_price.to_csv('BTC_price.csv', index=False)
eth_price.to_csv('ETH_price.csv', index=False)
sol_price.to_csv('SOL_price.csv', index=False)

# Verifikasi
for name, df in [('BTC', btc_price), ('ETH', eth_price), ('SOL', sol_price)]:
    print(f"{name}: {df.shape}, {df['Date'].iloc[0]} to {df['Date'].iloc[-1]}")

print("Selesai. File tersimpan.")