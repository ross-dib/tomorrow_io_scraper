"""
Data validation model for weather data response from tomorrow.io
using Pydantic models --> https://docs.pydantic.dev/latest/concepts/models/
"""
from pydantic import BaseModel, Field, field_validator, ValidationError
import datetime
from datetime import datetime as datetime_cls
import itertools


class TomorrowIOTimelineData(BaseModel):
    dew_point: float = Field(alias='dewPoint', default=None) # example val: 13
    humidity: float = Field(default=None)# example val: 78
    precipitation_intensity: float = Field(alias='precipitationIntensity', default=None) # example val: 0
    precipitation_probability: float = Field(alias='precipitationProbability', default=None) # example val: 0
    precipitation_type: int = Field(alias='precipitationType', default=None) # example val: 0
    temperature: float = Field(default=None)# example val: 16.88
    temperature_apparent: float = Field(alias='temperatureApparent', default=None) # example val: 16.88
    uv_index: float = Field(alias='uvIndex', default=None) # example val: 2
    wind_direction: float = Field(alias='windDirection', default=None) # example val: 218
    wind_gust: float = Field(alias='windGust', default=None) # example val: 5.31
    wind_speed: float = Field(alias='windSpeed', default=None) # example val: 3.38

    @field_validator('humidity')
    def validate_humidity(cls, humidity: int):
        '''Example of a custom validation on a field'''

        if humidity < 0:
            raise ValidationError(f"Received negative value for huimidity field. Value: {humidity}")
        return humidity


class TomorrowIOWeatherData(BaseModel):
    start_time: datetime_cls = Field(alias='startTime')  # example val: 2024-05-21 15:00:00+00:00
    latitude: float
    longitude: float
    data_load_date: datetime_cls = Field(default_factory=lambda: datetime_cls.now(datetime.UTC))
    values: TomorrowIOTimelineData


def unload_model_to_tuple(weather_data: TomorrowIOWeatherData) -> tuple:
    weather_data_json = weather_data.model_dump()
    metadata_tuple = tuple(weather_data_json.values())[:4]
    timeline_tuple = tuple(tuple(weather_data_json.values())[4].values())
    joined_tuple = tuple(itertools.chain(metadata_tuple, timeline_tuple))
    return joined_tuple
