import s3fs
from s3fs.core import S3FileSystem
import pandas as pd

def transform_data():
    s3 = S3FileSystem()
    # S3 bucket directory (data lake)
    DIR = 's3://ece5984-bucket-gasser18/Project/kickstats-stream'

    # List all the JSON files in the S3 folder
    json_files = s3.glob(DIR + '/*.json')

    # Create an empty DataFrame to store the combined data
    raw_data = pd.DataFrame()

    # Loop through the JSON files in the S3 bucket
    for file_path in json_files:
        with s3.open(file_path, 'r') as file:
            # Read JSON content from the file in S3
            json_string = file.read()

            # Remove leading and trailing quotes, then decode encoded characters
            json_string = json_string.strip('"').encode().decode('unicode-escape')

            # Read the modified JSON string into a DataFrame
            data = pd.read_json(json_string)

            # Append data to the existing DataFrame
            raw_data = raw_data._append(data, ignore_index=True)

    # Replace NaN values in 'Home Team Score', 'Away Team Score', and 'Minutes Played' columns with 0
    nan_columns = ['Home Team Score', 'Away Team Score', 'Minutes Played']
    for col in nan_columns:
        raw_data[col].fillna(0, inplace=True)

    # Find the index of the most recent occurrence of each fixture based on 'Minutes Played'
    most_recent_fixtures_indices = raw_data.groupby('Fixture ID')['Minutes Played'].idxmax()

    # Select the rows corresponding to the identified indices
    most_recent_fixtures = raw_data.loc[most_recent_fixtures_indices]

    # Dividing the raw dataset for each league
    grouped_by_league = most_recent_fixtures.groupby('League ID')

    # Push cleaned data to S3 bucket warehouse as a CSV file for each league
    DIR_wh = 's3://ece5984-bucket-gasser18/Project/kickstats-transform'
    for league_id, data in grouped_by_league:
        # Writing the CSV data to S3 including the index
        with s3.open('{}/{}_{}.csv'.format(DIR_wh, 'clean_kickstats', league_id), 'wb') as f:
            data.to_csv(f, index=True, encoding='utf-8')
