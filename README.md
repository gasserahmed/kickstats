# KickStats: Visualizing Live Football Scores
## Purpose
The purpose of this project is to provide football enthusiasts with real-time access to live scores of multiple football matches from various leagues and competitions. It addresses the problem of football fans needing a convenient and centralized platform to track ongoing matches, their scores, and relevant statistics. By offering a streamlined visualization of live scores, this project aims to enhance the football-watching experience and keep fans informed.

## Dataset
We are using the [API- FOOTBALL's](https://www.api-football.com/) Fixtures dataset.

## Pipeline / Architecture
For this project, we are using the following Stream-Visualization pipeline:
1. Data Ingestion: We retrieve real-time football match data from the API-Football API.
2. Stream Ingestion (Extract and Load): Using Apache Kafka, we ingest and stream the live data to ensure we have the latest scores and updates.
3. Data Storage: The ingested data is stored in Amazon S3 in JSON format, forming a data lake that allows for scalable and cost-effective storage.
4. Data Transformation: Pandas, a powerful Python library for data manipulation, is used to transform the raw data into a structured format suitable for analysis.
5. Data Warehousing: The transformed data is further stored in an Amazon S3 bucket in a CSV format, serving as our data warehouse for historical data analysis.
6. Relational Database: We use MySQL utilizing CSV importing to maintain a relational database for structured data storage and querying.
7. Data Analytics: Tableau is employed to create interactive dashboards and visualizations, enabling users to access live football match scores with ease.
![Pipeline](https://github.com/gasserahmed/kickstats/blob/main/images/Pipeline.png)

## Data Quality Assessment
The data fetched from the "KickStats" app is mostly clean, yet it needs slight preprocessing to optimize it for visualization. This involves several steps:
1. Partitioning by League: Dividing the raw dataset into specific segments, organized by league.
2. Handling Null Scores and Minutes Played: Replacing empty values (NaN) in scores and minutes played with zeros for consistency.
3. De-duplication of Fixtures: Streamlining the dataset by retaining the most recent occurrence of each fixture based on the 'Minutes Played' attribute, eliminating duplicate entries.
4. Handling Encoding and Decoding: Removing leading and trailing quotes while decoding encoded characters from JSON files, ensuring uniformity and clarity in the dataset.

## Data Transformation Models Used
The data transformation process involves multiple steps facilitated by Python and the Pandas library:
1. Data Retrieval: Utilizing the S3FileSystem library, the code accesses JSON files stored in an S3 bucket (kickstats-stream).
2. Data Aggregation: JSON content from multiple files is merged into a Pandas DataFrame (raw_data).
3. Cleaning & Formatting: The data is cleaned by handling missing values in specific columns ('Home Team Score', 'Away Team Score', 'Minutes Played') and is formatted for further analysis.
4. Fixture Identification: The code identifies the most recent occurrence of each fixture based on the 'Minutes Played' column.
5. Data Segmentation: The transformed data is segmented by 'League ID' using Pandas' groupby function.

## Final Result
The transformation code successfully aggregates, cleans, and segments live football match data retrieved from the "KickStats" app's API endpoint:
- Data is processed, cleaned, and organized into separate CSV files for each league based on 'League ID'.
- These CSV files are stored in the S3 bucket directory (kickstats-transform) to enable easy access and analysis.
- Further, the CSV files are imported into Tableau's database for seamless integration and visualization.
- Utilizing Tableau's functionalities, a comprehensive dashboard was created to display live football scores and statistics.
- The resulting Tableau dashboard provides an interactive and intuitive interface, allowing users to explore real-time match statistics and gain insights into ongoing football matches.
![Tableau Dashboard](https://github.com/gasserahmed/kickstats/blob/main/images/Tableau%20Dashboard.png)

## Code
[https://github.com/gasserahmed/kickstats](https://github.com/gasserahmed/kickstats)

## Thorough Investigation



