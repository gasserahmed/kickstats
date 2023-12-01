# KickStats: Visualizing Live Football Scores
## Purpose
The purpose of this project is to provide football enthusiasts with real-time access to live scores of multiple football matches from various leagues and competitions. It addresses the problem of football fans needing a convenient and centralized platform to track ongoing matches, their scores, and relevant statistics. By offering a streamlined visualization of live scores, this project aims to enhance the football-watching experience and keep fans informed.

## Dataset
We are using the [API- FOOTBALL's](https://www.api-football.com/) Fixtures dataset.

## Pipeline / Architecture
For this project, we are using the following Stream-Visualization pipeline:
  1. **Data Ingestion:** We retrieve real-time football match data from the API-Football API.
  2. **Stream Ingestion (Extract and Load):** Using Apache Kafka, we ingest and stream the live data to ensure we have the latest scores and updates.
  3. **Data Storage:** The ingested data is stored in Amazon S3 in JSON format, forming a data lake that allows for scalable and cost-effective storage.
  4. **Data Transformation:** Pandas, a powerful Python library for data manipulation, is used to transform the raw data into a structured format suitable for analysis.
  5. **Data Warehousing:** The transformed data is further stored in an Amazon S3 bucket in a CSV format, serving as our data warehouse for historical data analysis.
  6. **Relational Database:** We use MySQL utilizing CSV importing to maintain a relational database for structured data storage and querying.
  7. **Data Analytics:** Tableau is employed to create interactive dashboards and visualizations, enabling users to access live football match scores with ease.
![Pipeline](https://github.com/gasserahmed/kickstats/blob/main/images/Pipeline.png)

## Data Quality Assessment
The data fetched from the "KickStats" app is mostly clean, yet it needs slight preprocessing to optimize it for visualization. This involves several steps:
  1. **Partitioning by League:** Dividing the raw dataset into specific segments, organized by league.
  2. **Handling Null Scores and Minutes Played:** Replacing empty values (NaN) in scores and minutes played with zeros for consistency.
  3. **De-duplication of Fixtures:** Streamlining the dataset by retaining the most recent occurrence of each fixture based on the 'Minutes Played' attribute, eliminating duplicate entries.
  4. **Handling Encoding and Decoding:** Removing leading and trailing quotes while decoding encoded characters from JSON files, ensuring uniformity and clarity in the dataset.

## Data Transformation Models Used
The data transformation process involves multiple steps facilitated by Python and the Pandas library:
  1. **Data Retrieval:** Utilizing the S3FileSystem library, the code accesses JSON files stored in an S3 bucket (kickstats-stream).
  2. **Data Aggregation:** JSON content from multiple files is merged into a Pandas DataFrame (raw_data).
  3. **Cleaning & Formatting:** The data is cleaned by handling missing values in specific columns ('Home Team Score', 'Away Team Score', 'Minutes Played') and is formatted for further analysis.
  4. **Fixture Identification:** The code identifies the most recent occurrence of each fixture based on the 'Minutes Played' column.
  5. **Data Segmentation:** The transformed data is segmented by 'League ID' using Pandas' groupby function.

## Final Result
The transformation code successfully aggregates, cleans, and segments live football match data retrieved from the "KickStats" app's API endpoint:
  1. Data is processed, cleaned, and organized into separate CSV files for each league based on 'League ID'.
  2. These CSV files are stored in the S3 bucket directory (kickstats-transform) to enable easy access and analysis.
  3. Further, the CSV files are imported into Tableau's database for seamless integration and visualization.
  4. Utilizing Tableau's functionalities, a comprehensive dashboard was created to display live football scores and statistics.
  5. The resulting Tableau dashboard provides an interactive and intuitive interface, allowing users to explore real-time match statistics and gain insights into ongoing football matches.
![Tableau Dashboard](https://github.com/gasserahmed/kickstats/blob/main/images/Tableau%20Dashboard.png)

## Code
[https://github.com/gasserahmed/kickstats](https://github.com/gasserahmed/kickstats)

## Special Instructions for Code Execution:
To execute the code and reproduce the project's functionality:
1. **Access to "KickStats" App API:** Sign up for access to the "KickStats" app's API on Rapid API and obtain the required API key for making endpoint calls.
2. **Kafka Setup:** Set up Kafka to handle data streaming and ingestion. Ensure proper configurations for Kafka producers and consumers as per the project specifications.
3. **Amazon S3 Configuration:** Establish an S3 bucket on AWS and configure it to receive and store the streamed data. Adjust permissions and access controls as needed.
4. **Python Environment and Apache Airflow:**
    - Ensure Python and required libraries (S3FileSystem, Pandas) are installed in your development environment.
    - Install and configure Apache Airflow in your environment to handle orchestration and scheduling of data processing tasks.
6. **Airflow DAG Setup:**
    1. Place the provided DAG configurations (stream_ingest_dag and transform_dag) into the appropriate Airflow DAGs folder.
    2. Update stream_ingest.py and transform.py with the corresponding functions (kafka_consumer and transform_data) for ingestion and transformation.
    3. Start the Airflow scheduler and webserver to enable DAG execution.
7. **Execute DAGs & Python Scripts:**
    1. Initiate the stream_ingest_dag in Airflow to activate Kafka consumers for data ingestion.
    2. Utilize produce.py to stream data as JSON into the designated S3 storage.
    3. Trigger the transform_dag within Airflow to perform data transformation, segmenting it into distinct CSV files based on league IDs, and subsequently, upload the results to S3 for storage.
8. **Monitoring & Iteration:** Regularly monitor data updates and re-run the script or trigger DAGs in Airflow as necessary to maintain up-to-date CSV files in the S3 bucket.

## Thorough Investigation
### Viability Assessment and Scaling Recommendations:
- **Project Viability:** The pilot phase successfully demonstrated the capability to process real-time football match data through streamlined ingestion, transformation, and storage in a scalable manner, underscoring the project's initial viability.
- **Scaling Considerations:** Scaling up demands strengthening the pipeline's robustness to handle increased data volumes during peak match times. Strategies entail load balancing and optimizing resource allocation for Kafka, S3 storage, and transformation tasks.

### Assessment of Innovativeness:
- **Innovative Approach:** The project innovatively processes and stores real-time data efficiently, offering immediate insights into live football match statistics. Apache Airflow integration enhances orchestration and task scheduling, adding sophistication to the project's architecture.
- **Technical and Platform Concerns:**
  - **Technical Challenges:** Potential hurdles might arise in managing sudden data spikes during high-traffic matches, impacting real-time updates. Addressing these necessitates fine-tuning Kafka configuration and optimizing S3 storage for increased throughput.
  - **Platform Considerations:** While the project thrives in processing data, limitations emerged with Tableau integration. Technical constraints resulted in challenges with automated visualization due to manual data importing, hindering the seamless display of real-time statistics without manual intervention.

### Recommendations for Next Steps:
- **Enhanced Data Sources::** Expanding data sources beyond match scores to include player stats, team performance trends, and historical data for comprehensive analysis.
- **Visualization Enhancement:**
  - Considering Tableau limitations, exploring alternative visualization tools or developing a custom visualization solution integrated with the existing pipeline could automate data import from processed CSV files. This would ensure real-time insights without manual intervention.
  - Implementing predictive analytics, match simulations, and dynamic forecasting features to offer deeper insights to users.
- **AI Integration:** Incorporating machine learning models for match outcome predictions and player performance analysis could enrich the project's capabilities.

### Conclusion and Future Direction:
With Tableau limitations in mind, the focus should center on enhancing the data processing pipeline and exploring/developing a more seamless visualization solution. This evolution will transition the project into a sophisticated real-time sports analytics platform, offering automated, dynamic, and insightful visualizations for diverse user needs and engagement.


