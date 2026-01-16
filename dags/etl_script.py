import os
import boto3
import pandas as pd
import requests
from datetime import datetime
from io import BytesIO

# CONFIGURATION
MINIO_ENDPOINT = os.getenv('MINIO_ENDPOINT')
ACCESS_KEY = os.getenv('MINIO_ACCESS_KEY')
SECRET_KEY = os.getenv('MINIO_SECRET_KEY')
BUCKET_NAME = os.getenv('BUCKET_NAME')

def extract_and_load():
    # 1. FETCH DATA
    print("Fetching data from CoinGecko...")
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {'vs_currency': 'usd', 'order': 'market_cap_desc', 'per_page': 50, 'page': 1}
    response = requests.get(url, params=params)
    data = response.json()
    
    # 2. CONVERT TO PARQUET
    df = pd.DataFrame(data)
    # Add extraction timestamp
    df['extracted_at'] = datetime.now()
    
    # Create Buffer
    out_buffer = BytesIO()
    df.to_parquet(out_buffer, index=False)
    
    # 3. UPLOAD TO MINIO
    s3 = boto3.client('s3',
                      endpoint_url=MINIO_ENDPOINT,
                      aws_access_key_id=ACCESS_KEY,
                      aws_secret_access_key=SECRET_KEY)
    
    # Dynamic Path: raw/coingecko/YYYY/MM/DD/data.parquet
    today = datetime.now()
    path = f"raw/coingecko/{today.year}/{today.month:02d}/{today.day:02d}/data.parquet"
    
    print(f"Uploading to {BUCKET_NAME}/{path}...")
    try:
        s3.put_object(Bucket=BUCKET_NAME, Key=path, Body=out_buffer.getvalue())
        print("Success.")
    except Exception as e:
        print(f"Failed: {e}")

if __name__ == "__main__":
    extract_and_load()