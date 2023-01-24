import os
import pandas as pd
import argparse
from sqlalchemy import create_engine
from time import time

def main(params):
    user = params.user
    host = params.host
    port = params.port
    password = params.password
    db = params.db
    table_name = params.table_name
    url = params.url

    csv_name = 'data.csv.gz'

    # download csv file
    os.system(f"wget {url} -O {csv_name}")
      
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

    df_iter = pd.read_csv(csv_name, compression='gzip', on_bad_lines='skip', iterator=True, chunksize=100000)
    df = next(df_iter)

    df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
    df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

    df.head(n=0).to_sql(name=table_name, con=engine, if_exists='replace')

    for df in df_iter:
        t_start = time()
        
        df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
        df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)
        
        df.to_sql(name=table_name, con=engine, if_exists='append')
        
        t_end = time()
        
        print('inserted another chunk, took %3.f second' %(t_end - t_start))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = 'Ingest CSV data to Postgres')

    parser.add_argument('--user', help='username for postgres')
    parser.add_argument('--host', help='host for postgres')
    parser.add_argument('--port', help='port for postgres')
    parser.add_argument('--password', help='password for postgres')
    parser.add_argument('--db', help='database name for postgres')
    parser.add_argument('--table_name', help='table name for postgres')
    parser.add_argument('--url', help='url for csv file')

    args = parser.parse_args()

    main(args)

