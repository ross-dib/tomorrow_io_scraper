# Tomorrow.io Weather Scraper
This simple python app is a lightweight data pipeline that scrapes data from [tomorrow.io](tomorrow.io). See [the issues tab](https://github.com/ross-dib/tomorrow_io_scraper/issues) for proposed improvements and bugs.

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

## Development
1. Install [Docker](https://docs.docker.com/get-docker/)
2. Install [postrgeSQL](https://www.postgresql.org/download/)
3. Create local postgreSQL DB and table:
```
createdb <INSERT DB NAME>
psql <INSERT DB NAME>
```
- this will bring you to an interactive postgres session. Copy the commands from [scripts/init-db.sql](https://github.com/ross-dib/tomorrow_io_scraper/blob/main/scripts/init-db.sql) and run them in the shell
4. Get an API key from [tomorrow.io](https://app.tomorrow.io/home) (free-tier will suffice) and set it as an environment variable: 
```
export TOMORROW_API_KEY=<INSERT KEY>
```
5. You can now run the app locally and see results in the psql session
```
python -m weather_scraper
```

### Testing







