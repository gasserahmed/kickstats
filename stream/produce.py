import time
import pandas as pd
from kafka import KafkaProducer
from json import dumps
import requests


def kafka_producer():
    # Get fixtures in progress from API-FOOTBALL
    url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
    querystring = {"live": "all"}
    headers = {
        "X-RapidAPI-Key": "fc0de02817mshcbe1abaddafd796p15cad8jsn1d671d61614e",
        "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    fixtures_in_progress = response.json().get("response")

    # Kafka Producer
    producer = KafkaProducer(bootstrap_servers=['54.196.246.52:9134'],  # change ip and port number here
                             value_serializer=lambda x:
                             dumps(x).encode('utf-8'))

    t_end = time.time() + 60 * 1  # Amount of time data is sent for in seconds
    while time.time() < t_end:
        df_stream = pd.DataFrame(columns=["Home Team Name", "Home Team Logo", "Home Team Score",
                                          "Away Team Name", "Away Team Logo", "Away Team Score",
                                          "Period", "Minutes Played"])
        for fixture in fixtures_in_progress:
            home_team = fixture.get("teams").get("home")
            away_team = fixture.get("teams").get("away")
            new_row = {
                "Home Team Name": home_team.get("name"),
                "Home Team Logo": home_team.get("logo"),
                "Home Team Score": fixture.get("goals").get("home"),
                "Away Team Name": away_team.get("name"),
                "Away Team Logo": away_team.get("logo"),
                "Away Team Score": fixture.get("goals").get("away"),
                "Period": fixture.get("fixture").get("status").get("long"),
                "Minutes Played": fixture.get("fixture").get("status").get("elapsed")
            }
            df_stream = df_stream._append(new_row, ignore_index=True)
            producer.send('KickStatsData', value=df_stream.to_json())  # Add topic name here
    print("done producing")

kafka_producer()
