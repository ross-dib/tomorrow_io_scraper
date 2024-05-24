# Tomorrow.io Weather Scraper
This simple python app is a lightweight data pipeline that scrapes data from [tomorrow.io](tomorrow.io). 

## Usage
1. Install [Docker](https://docs.docker.com/get-docker/)

2. Get an API key from [tomorrow.io](https://app.tomorrow.io/home) (free-tier will suffice) and set it as an environment variable: 
```console
export TOMORROW_API_KEY=<INSERT KEY>
```
3. Run `docker compose`
```console
docker compose up --build 
```
4. Navigate to [localhost:8888](http://localhost:8888/notebooks/tomorrow_io_analysis.ipynb) to view data via Jupyter Notebook
5. To tear containers down, run ```docker compose down --volumes``` 

## Development
1. Install [Docker](https://docs.docker.com/get-docker/)
2. Install [postrgeSQL](https://www.postgresql.org/download/)
3. Install [Python 3.12](https://www.python.org/downloads/release/python-3120/)
4. Install [pipenv](https://pipenv.pypa.io/en/latest/installation.html)
   1. Once installed, run the following: ```pipenv install --dev```
5. Create local postgreSQL DB and table:
```
createdb <INSERT DB NAME>
psql <INSERT DB NAME>
```
- this will bring you to an interactive postgres session. Copy the commands from [scripts/init-db.sql](https://github.com/ross-dib/tomorrow_io_scraper/blob/main/scripts/init-db.sql) and run them in the shell
6. Get an API key from [tomorrow.io](https://app.tomorrow.io/home) (free-tier will suffice) and set it as an environment variable: 
```
export TOMORROW_API_KEY=<INSERT KEY>
```
7. You can now run the app locally and see results in the `psql` interactive session
```
python -m weather_scraper
```

### Testing
1. Follow steps in [development](##Development) section above
2. Run ```pipenv run python -m pytest --junit-xml=junit_xml_test_report.xml --cov-branch --cov weather_scraper/ tests``` for unit tests with coverage


## Deicions and Improvements
NOTE: See [the issues tab](https://github.com/ross-dib/tomorrow_io_scraper/issues) for specific code references to improvements and bugs.

### Database
- I chose to use a postgres relational database to store the weather data. The brief description of the use case didn't provide much to go off of in terms of choosing a datastore, so something that is open-source and commonly used with jupyter appeared to be a safe choice for a proof-of-concept.
- Given more information about the end user / use case, here are some alternatives:
  - time-series specific database
    - I did some light reading about time-series specific databases like InfluxData and Timescale (though the readings were company blogs, so effectively marketing material). These databases could make analysis simpler, though I'm not familiar enough with Time-Series data analysis to judge whether they'd be worth it. 
  - Data Warehouse
    - If this data is to be used for OLAP (analytical) use cases only and it is expected to grow into the TB or PB range, a data warehouse like AWS Redshift or Snowflake could be a good alternative. These are the type of data stores I'm more familiar with (more specifically, proprietary data lake / data lakehouse).
    - Scalability and performance are major benefits of a data warehouse while high cost / complexity can be a concern, depending on scale 
- NoSQL database
  - Given this data is highly structured, I'm not sure non-relational databases are a benefit here. They _can_ make analysis harder, and flexibility in schema doesn't seem to be a benefit unless a different end use case is introduced. 

### Compute
- This is a single process running on a single container. This code could be extended to run on a containerized compute framework like AWS ECS / Fargate / Kubernetes or a serverless solution like AWS Lambda 
  - Parallelization would help if the use case called for expanding to many more geolocations as these processes could run in parallel. Frameworks such as Dask in Python could be used here.
- Either batch or event driven architecture could be used as well. 
  - For batch, it appears tomorrow.io releases this data on consistent schedule, so workers could spin up and hit the weather endpoints in sync with this schedule.
  - For event, there's an [Alert API](https://docs.tomorrow.io/reference/overview-alerts) provided by tomorrow.io if specific weather information is of interest.
  - Both of these architectures could use a message queue such as AWS SQS (+ dead-letter queue for failure handling) to decouple the scheduling layer with the processing layer, allowing for more horizontal scalability






