import argparse
import sys
import logging
from weather_scraper.clients.tomorrow_io import TomorrowIOClient, TomorrowIOWeatherData
from weather_scraper.clients.postgres_db import PostrgresClient


def main():
    # set API params
    timesteps = ["1h"]
    fields = ["temperature",
              "humidity",
              "temperatureApparent",
              "dewPoint",
              "humidity",
              "windSpeed",
              "windDirection",
              "windGust",
              "precipitationIntensity",
              "precipitationProbability",
              "precipitationType",
              "uvIndex"]
    start_time = "nowMinus1d"
    end_time = "nowPlus5d"

    locations = [
        ["25.8600", "-97.4200"],
        ["25.9000", "-97.5200"],
        ["25.9000", "-97.4800"],
        ["25.9000", "-97.4400"],
        ["25.9000", "-97.4000"],
        ["25.9200", "-97.3800"],
        ["25.9400", "-97.5400"],
        ["25.9400", "-97.5200"],
        ["25.9400", "-97.4800"],
        ["25.9400", "-97.4400"]
    ]

    weather_data: list[TomorrowIOWeatherData] = TomorrowIOClient(timesteps, fields, start_time, end_time, locations)\
        .get_weather_data()
    PostrgresClient().load(weather_data)


if __name__ == "__main__":  # pragma: no cover
    main()