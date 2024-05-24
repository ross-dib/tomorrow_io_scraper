import pytest
from mockito import mock, when, verify, unstub
from weather_scraper.clients.tomorrow_io import TomorrowIOClient
from weather_scraper.models.tomorrow_response import ValidationError, TomorrowIOWeatherData
import requests
import datetime


@pytest.mark.parametrize("mock_api_response,expected_result", [
    pytest.param(
        {'data': {
            'timelines': [
                {'timestep': '1h', 'endTime': '2024-05-29T16:00:00Z', 'startTime': '2024-05-23T16:00:00Z',
                 'intervals': [
                     {'startTime': '2024-05-23T16:00:00Z', 'values': {'dewPoint': 24.5, 'humidity': 66, 'precipitationIntensity': 0, 'precipitationProbability': 0, 'precipitationType': 0, 'temperature': 31.69, 'temperatureApparent': 38.17, 'uvIndex': 6, 'windDirection': 161, 'windGust': 12.88, 'windSpeed': 8.81}},
                 ]
                 }
            ]
        }},
        [[{'startTime': '2024-05-23T16:00:00Z', 'values': {'dewPoint': 24.5, 'humidity': 66, 'precipitationIntensity': 0, 'precipitationProbability': 0, 'precipitationType': 0, 'temperature': 31.69, 'temperatureApparent': 38.17, 'uvIndex': 6, 'windDirection': 161, 'windGust': 12.88, 'windSpeed': 8.81}, 'latitude': '25.8600', 'longitude': '-97.4200'}]]),
    pytest.param(
        {'data': {
            'timelines': [
                {'timestep': '1h', 'endTime': '2024-05-29T15:00:00Z', 'startTime': '2024-05-23T15:00:00Z',
                 'intervals': [
                     {'startTime': '2024-05-23T16:00:00Z',
                      'values': {'dewPoint': 24.5, 'humidity': 66, 'precipitationIntensity': 0,
                                 'precipitationProbability': 0, 'precipitationType': 0, 'temperature': 31.69,
                                 'temperatureApparent': 38.17, 'uvIndex': 6, 'windDirection': 161, 'windGust': 12.88,
                                 'windSpeed': 8.81}},
                     {'startTime': '2024-05-23T17:00:00Z',
                      'values': {'dewPoint': 23.38, 'humidity': 59, 'precipitationIntensity': 0,
                                 'precipitationProbability': 0, 'precipitationType': 0, 'temperature': 32.38,
                                 'temperatureApparent': 37.65, 'uvIndex': 9, 'windDirection': 156.19, 'windGust': 12.81,
                                 'windSpeed': 9.5}}
                 ]
                 }
            ]
        }},
        [[{'startTime': '2024-05-23T16:00:00Z', 'values': {'dewPoint': 24.5, 'humidity': 66, 'precipitationIntensity': 0, 'precipitationProbability': 0, 'precipitationType': 0, 'temperature': 31.69, 'temperatureApparent': 38.17, 'uvIndex': 6, 'windDirection': 161, 'windGust': 12.88, 'windSpeed': 8.81}, 'latitude': '25.8600', 'longitude': '-97.4200'}, {'startTime': '2024-05-23T17:00:00Z', 'values': {'dewPoint': 23.38, 'humidity': 59, 'precipitationIntensity': 0, 'precipitationProbability': 0, 'precipitationType': 0, 'temperature': 32.38, 'temperatureApparent': 37.65, 'uvIndex': 9, 'windDirection': 156.19, 'windGust': 12.81, 'windSpeed': 9.5}, 'latitude': '25.8600', 'longitude': '-97.4200'}]]
    )
])
def test__get_data_and_format(mock_api_response: dict, expected_result: list[list]):
    # params for TomorrowIOClient constructor
    timesteps = ["1h"]
    fields = ["temperature", "humidity"]
    start_time = "nowMinus1d"
    end_time = "nowPlus5d"
    locations = [["25.8600", "-97.4200"]]

    client = TomorrowIOClient(timesteps, fields, start_time, end_time, locations)

    # create mock response
    mock_response = mock({
        'status_code': 200,
        'json': lambda: mock_api_response,
        'raise_for_status': lambda: None
    }, spec=requests.Response)

    # define mock
    when(client._session).post(...).thenReturn(mock_response)

    result = client._get_data_and_format()
    assert result == expected_result
    unstub()


@pytest.mark.parametrize("mock_input_data,expected_result", [
    pytest.param([[{'startTime': '2024-05-23T16:00:00Z', 'values': {'dewPoint': 24.5, 'humidity': -66, 'precipitationIntensity': 0, 'precipitationProbability': 0, 'precipitationType': 0, 'temperature': 31.69, 'temperatureApparent': 38.17, 'uvIndex': 6, 'windDirection': 161, 'windGust': 12.88, 'windSpeed': 8.81}, 'latitude': '25.8600', 'longitude': '-97.4200'}]],
                 [] # negative humidity, should raise Validation error and return empty list
    )
])
def test_parse_and_validate_data(mock_input_data: list[list], expected_result):
    # params for TomorrowIOClient constructor
    timesteps = ["1h"]
    fields = ["temperature", "humidity"]
    start_time = "nowMinus1d"
    end_time = "nowPlus5d"
    locations = [["25.8600", "-97.4200"]]

    client = TomorrowIOClient(timesteps, fields, start_time, end_time, locations)

    result: list[TomorrowIOWeatherData] = client._parse_and_validate_data(mock_input_data)

    assert (result == expected_result) or ([i.model_dump() for i in result] == expected_result)

    # Clean up
    unstub()
