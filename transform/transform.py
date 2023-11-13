import s3fs
from s3fs.core import S3FileSystem
import numpy as np
import pickle
import json #TODO: remove before airflow
import pandas as pd #TODO: remove before airflow

def transform_data():

    s3 = S3FileSystem()
    # S3 bucket directory (data lake)
    DIR = 's3://ece5984-bucket-gasser18/Project/kickstats-stream'
    # Get data from S3 bucket as a pickle file
    #raw_data = np.load(s3.open('{}/{}'.format(DIR, 'kickstats_data_0.json')))
    raw_data = pd.read_json('../kickstats_data_0.json')


    # Dividing the raw dataset for each company individual company
    raw_data.columns = raw_data.columns.swaplevel(0,1)
    raw_data.sort_index(axis=1, level=0, inplace=True)
    df_aapl_rw = raw_data['AAPL']
    df_amzn_rw = raw_data['AMZN']
    df_googl_rw = raw_data['GOOGL']

    # Dropping rows with NaN in them
    df_aapl = df_aapl_rw.dropna()
    df_amzn = df_amzn_rw.dropna()
    df_googl = df_googl_rw.dropna()


    # Removing rows with outliers
    for col in list(df_aapl.columns)[0:4]:                                          # We ignore 'Volume' column
        df_aapl = df_aapl.drop(df_aapl[df_aapl[col].values > 900].index)            # Values above 900 are dropped
        df_aapl = df_aapl.drop(df_aapl[df_aapl[col].values < 0.001].index)          # Values below 0.001 are dropped

    # Dropping duplicate rows
    df_aapl = df_aapl.drop_duplicates()

    # Push cleaned data to S3 bucket warehouse
    DIR_wh = 's3://ece5984-bucket-gasser18/Project/kickstats-transform'
    with s3.open('{}/{}'.format(DIR_wh, 'clean_kickstats.pkl'), 'wb') as f:
        f.write(pickle.dumps(df_aapl))


transform_data() #TODO: REMOVE THIS BEFORE GOING TO AIRFLOW
