import time
import pandas as pd
from kafka import KafkaProducer
from json import dumps
import requests
from datetime import datetime

def kafka_producer():
    # API-FOOTBALL headers
    current_date = datetime.now().strftime("%Y-%m-%d")
    url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
    querystring = {"date": current_date, "timezone": "America/New_York", }  # all today fixtures in NY timezone
    headers = {
        "X-RapidAPI-Key": "fc0de02817mshcbe1abaddafd796p15cad8jsn1d671d61614e",
        "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
    }

    # Kafka Producer
    producer = KafkaProducer(bootstrap_servers=['3.235.223.243:9140'],  # change ip and port number here
                             value_serializer=lambda x:
                             dumps(x).encode('utf-8'))

    t_end = time.time() + 60 * 10  # Amount of time data is sent for in seconds
    while time.time() < t_end:
        # Get today's fixtures from API-FOOTBALL
        response = requests.get(url, headers=headers, params=querystring)
        today_fixtures = response.json().get("response")

        # Prepare the dataframe
        df_stream = pd.DataFrame(columns=["Fixture ID", "Date", "Country",
                                          "League ID", "League Name", "League Logo",
                                          "Home Team Name", "Home Team Logo", "Home Team Score",
                                          "Away Team Name", "Away Team Logo", "Away Team Score",
                                          "Status", "Minutes Played"])
        for fixture in today_fixtures:
            # Extracting timestamp from the fixture's 'fixture' dictionary
            fixture_info = fixture.get("fixture", {})
            fixture_id = fixture_info.get("id")
            timestamp = fixture_info.get("timestamp")

            league = fixture.get("league")
            home_team = fixture.get("teams").get("home")
            away_team = fixture.get("teams").get("away")
            new_row = {
                "Fixture ID": fixture_id,
                "Date": timestamp,
                "Country": league.get("country"),
                "League ID": league.get("id"),
                "League Name": league.get("name"),
                "League Logo": league.get("logo"),
                "Home Team Name": home_team.get("name"),
                "Home Team Logo": home_team.get("logo"),
                "Home Team Score": fixture.get("goals").get("home"),
                "Away Team Name": away_team.get("name"),
                "Away Team Logo": away_team.get("logo"),
                "Away Team Score": fixture.get("goals").get("away"),
                "Status": fixture.get("fixture").get("status").get("long"),
                "Minutes Played": fixture.get("fixture").get("status").get("elapsed")
            }
            df_stream = df_stream._append(new_row, ignore_index=True)

        producer.send('KickStatsData', value=df_stream.to_json())  # Add topic name here
        time.sleep(60)  # Wait for 1 minute before getting another set of data from API-FOOTBALL
    print("done producing")

kafka_producer()
