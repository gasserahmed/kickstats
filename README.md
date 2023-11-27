# KickStats: Visualizing Live Football Scores
## Project's Function
The purpose of this project is to provide football enthusiasts with real-time access to live scores of multiple football matches from various leagues and competitions. It addresses the problem of football fans needing a convenient and centralized platform to track ongoing matches, their scores, and relevant statistics. By offering a streamlined visualization of live scores, this project aims to enhance the football-watching experience and keep fans informed.

## Dataset
We are using the [API- FOOTBALL's](https://www.api-football.com/) Fixtures dataset.

## Pipeline / Architecture
For this project, we are using the following Stream-Visualization pipeline:
1.	Data Ingestion: We retrieve real-time football match data from the API-Football API.
2.	Stream Ingestion (Extract and Load): Using Apache Kafka, we ingest and stream the live data to ensure we have the latest scores and updates.
3.	Data Storage: The ingested data is stored in Amazon S3 in JSON format, forming a data lake that allows for scalable and cost-effective storage.
4.	Data Transformation: Pandas, a powerful Python library for data manipulation, is used to transform the raw data into a structured format suitable for analysis.
5.	Data Warehousing: The transformed data is further stored in an Amazon S3 bucket in a CSV format, serving as our data warehouse for historical data analysis.
6.	Relational Database: We use MySQL utilizing CSV importing to maintain a relational database for structured data storage and querying.
7.	Data Analytics: Tableau is employed to create interactive dashboards and visualizations, enabling users to access live football match scores with ease.

## Data Quality Assessment
1. Partitioning by League: Dividing the raw dataset into specific segments, organized by league.

2. Handling Null Scores and Minutes Played: Replacing missing values (NaN) in scores and minutes played with zeros for consistency.

3. De-duplication of Fixtures: Streamlining the dataset by retaining the most recent occurrence of each fixture based on the 'Minutes Played' attribute, eliminating duplicate entries.

4. Handling Encoding and Decoding: Removing leading and trailing quotes while decoding encoded characters from JSON files, ensuring uniformity and clarity in the dataset.

## Data Transformation Models Used

## Infographic
![Pipeline](https://github.com/gasserahmed/kickstats/blob/main/images/Pipeline.png)

## Final Result
![Tableau Dashboard](https://github.com/gasserahmed/kickstats/blob/main/images/Tableau%20Dashboard.png)

## Code
[https://github.com/gasserahmed/kickstats](https://github.com/gasserahmed/kickstats)

## Thorough Investigation



