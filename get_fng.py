import requests
import pandas as pd

def get_fear_greed(start_str, end_str):
    start_ts = int(pd.Timestamp(start_str, tz='UTC').timestamp())
    end_ts   = int(pd.Timestamp(end_str, tz='UTC').timestamp())
    
    # Hitung jumlah hari
    days = (pd.Timestamp(end_str) - pd.Timestamp(start_str)).days + 2
    
    url = f"https://api.alternative.me/fng/?limit={days}&format=json"
    resp = requests.get(url).json()
    
    df = pd.DataFrame(resp['data'])
    df['Date'] = pd.to_datetime(df['timestamp'].astype(int), unit='s', utc=True).dt.normalize()
    df['fear_greed'] = df['value'].astype(int)
    df = df[['Date', 'fear_greed']].sort_values('Date').reset_index(drop=True)
    
    # Filter ke periode yang dibutuhkan
    start = pd.Timestamp(start_str, tz='UTC')
    end   = pd.Timestamp(end_str, tz='UTC')
    df = df[(df['Date'] >= start) & (df['Date'] <= end)].reset_index(drop=True)
    
    return df

fng = get_fear_greed('2020-10-01', '2026-03-19')
print(f"Shape: {fng.shape}")
print(f"Date range: {fng['Date'].iloc[0]} to {fng['Date'].iloc[-1]}")
print(f"Null: {fng.isnull().sum().sum()}")
print(fng.head())

# Simpan
fng.to_csv('FNG.csv', index=False)
print("Tersimpan ke FNG.csv")