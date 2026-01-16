import os
import boto3
import pandas as pd
from sqlalchemy import create_engine, text
from io import BytesIO
import json

# CONFIG
MINIO_ENDPOINT = os.getenv('MINIO_ENDPOINT')
ACCESS_KEY = os.getenv('MINIO_ACCESS_KEY')
SECRET_KEY = os.getenv('MINIO_SECRET_KEY')
BUCKET_NAME = os.getenv('BUCKET_NAME')

# Postgres Connection
DB_USER = os.getenv('POSTGRES_USER',)
DB_PASS = os.getenv('POSTGRES_PASSWORD')
DB_HOST = os.getenv('POSTGRES_HOST')
DB_NAME = os.getenv('POSTGRES_DB')
CONN_STR = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:5432/{DB_NAME}"

def load_to_warehouse():
    print("Starting Load Step: MinIO -> Postgres")
    
    # 1. Connect to MinIO
    s3 = boto3.client('s3', endpoint_url=MINIO_ENDPOINT,
                      aws_access_key_id=ACCESS_KEY,
                      aws_secret_access_key=SECRET_KEY)
    
    # 2. Find the latest file (Simple logic for now)
    objects = s3.list_objects_v2(Bucket=BUCKET_NAME, Prefix='raw/coingecko/')
    if 'Contents' not in objects:
        print("No data found in MinIO.")
        return

    # Get latest file based on LastModified timestamp
    latest_file = max(objects['Contents'], key=lambda x: x['LastModified'])
    print(f"Loading file: {latest_file['Key']}")
    
    # 3. Read Parquet into Pandas
    obj = s3.get_object(Bucket=BUCKET_NAME, Key=latest_file['Key'])
    df = pd.read_parquet(BytesIO(obj['Body'].read()))
        
    for col in df.columns:
        if df[col].dtype == 'object':
            # Check every cell; if it's a list or dict, convert to JSON string
            df[col] = df[col].apply(lambda x: json.dumps(x) if isinstance(x, (dict, list)) else x)
    
    # 4. Write to Postgres (Raw Schema)
    engine = create_engine(CONN_STR)

    # Ensure raw schema exists
    with engine.begin() as conn:
        conn.execute(text("CREATE SCHEMA IF NOT EXISTS raw;"))
    # Dump the data
    df.to_sql('source_coingecko', engine, schema='raw', if_exists='replace', index=False)
    print(f"Loaded {len(df)} rows into raw.source_coingecko")

if __name__ == "__main__":
    load_to_warehouse()