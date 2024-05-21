"""
API client for retrieveing weather data from https://www.tomorrow.io/
<Insert API endpoint>
"""

import requests


class TomorrowIOClient:
    def __init__(self):
        self._session = requests.Session()
        # add any session config here

    def get_weather_data(self, config_path: str) -> dict:
        # TODO
        # read location config and load into dict

        # make request to API using config above

        # load response into Pydantic model

        # return data in dict format (or Pydantic model?)
        #return
