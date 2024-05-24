"""
API client for retrieveing weather data from https://www.tomorrow.io/
For more info on this endpoint, see the docs --> https://docs.tomorrow.io/reference/post-timelines
"""

import requests
from requests.exceptions import HTTPError, RequestException
import time
import datetime
import os

from weather_scraper.utils import logger
from weather_scraper.models.tomorrow_response import TomorrowIOWeatherData, ValidationError

API_KEY = os.environ['TOMORROW_API_KEY']


class TomorrowIOClient:
    def __init__(self, timesteps: list, fields: list, start_time: str, end_time: str, locations: list[list]):
        self._session = requests.Session()
        self.logger = logger.get_logger()
        self.timesteps = timesteps
        self.fields = fields
        self.start_time = start_time
        self.end_time = end_time
        self.locations = locations

    def get_weather_data(self) -> list[TomorrowIOWeatherData]:
        """
        Public-facing orchestrator function that gets weather data and validates it
        :return: list of validated weather data
        """

        raw_data = self._get_data_and_format()
        validated_data = self._parse_and_validate_data(raw_data)
        return validated_data

    def _get_data_and_format(self) -> list:
        '''
        Sends an POST request to tomorrow.io Timeline API and
        correlates location data with weather data
        :return: list of responses from tomorrow.io Timeline API
        '''

        headers = {
            "accept": "application/json",
            "Accept-Encoding": "gzip",
            "content-type": "application/json"
        }
        url = f"https://api.tomorrow.io/v4/timelines?apikey={API_KEY}"

        historical_weather_list = []

        for location in self.locations:
            payload = {
                "location": ','.join(location),
                "fields": self.fields,
                "timesteps": self.timesteps,
                "startTime": self.start_time,
                "endTime": self.end_time,
            }

            try:
                response = self._session.post(url, json=payload, headers=headers)
                response.raise_for_status()
            except HTTPError as e:
                self.logger.error(f"Request to {url} failed for latitude: {location[0]}, longitude: {location[1]} \n "
                              f"Error code: {response.status_code}\n"
                              f"{response.reason}")
                self.logger.error(e)
                continue
            except RequestException as e:
                self.logger.error(f"Request to {url} failed with error {e}")
                self.logger.error(e)
                continue
            else:
                weather_intervals = response.json()['data']['timelines'][0]['intervals']
                # TODO: evaluate scalability of this iteration
                for interval in weather_intervals:
                    interval["latitude"] = location[0]
                    interval["longitude"] = location[1]
                historical_weather_list.append(weather_intervals)
            finally:
                time.sleep(0.5) # tomorrow.io's free plan rate limits at >3 TPS

        return historical_weather_list

    def _parse_and_validate_data(self, data: list) -> list:
        '''
        :param data: list of responses from tomorrow.io Timeline API
        :return: list of validated entries that fit the TomorrowIOTimelineData model
        '''
        validated_data = []
        for location in data:
            for entry in location:
                try:
                    valid_entry = TomorrowIOWeatherData(**entry)
                    validated_data.append(valid_entry)
                except ValidationError as e:
                    self.logger.error(f"Error validating tomorrow.io weather data for:\n"
                                      f"location: {location}"
                                      f"date: {entry['startTime']}")
                    self.logger.error(e)
                    continue
                except Exception as e:
                    self.logger.error(f"Unexpected error when parsing tomorrow.io response for {location}\n"
                                      f"Error: {e}")
                    continue

        return validated_data
