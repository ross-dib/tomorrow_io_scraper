DROP TABLE IF EXISTS tomorrow_io_timeline_data;
CREATE TABLE IF NOT EXISTS tomorrow_io_timeline_data (
                    start_time TIMESTAMP,
                    latitude FLOAT,
                    longitude FLOAT,
                    data_load_date TIMESTAMP,
                    dew_point FLOAT,
                    humidity FLOAT,
                    precipitation_intensity FLOAT,
                    precipitation_probability FLOAT,
                    precipitation_type FLOAT,
                    temperature_c FLOAT,
                    temperature_apparent_c FLOAT,
                    uv_index FLOAT,
                    wind_direction FLOAT,
                    wind_gust FLOAT,
                    wind_speed FLOAT,
                    PRIMARY KEY (start_time, latitude, longitude)
);