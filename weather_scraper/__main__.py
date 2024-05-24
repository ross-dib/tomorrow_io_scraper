import argparse
import sys
import logging
from weather_scraper.clients.tomorrow_io import TomorrowIOClient, TomorrowIOWeatherData
from weather_scraper.clients.postgres_db import PostrgresClient

def main():
    weather_data: list[TomorrowIOWeatherData] = TomorrowIOClient().get_weather_data()
    PostrgresClient().load(weather_data)

if __name__ == "__main__":  # pragma: no cover
    main()