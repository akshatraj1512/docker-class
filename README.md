# docker-postgres-101

## 1. Executing Local Scripts inside a Docker Container (Named Volumes).

- Prerequisites:

  `Python` and `Docker` installed and running.
  
- In terminal:

```bash
docker run -it --entrypoint=bash -v $(pwd)/test:/app/test python:3.13.1-slim
```
```bash
cd app/test
```
```bash
python script.py
```

## 2. Performing ETL with a simple pipeline 

- Prerequisites:

  Find in the `.toml` file.
  
- In terminal:

```bash
cd pipeline
uv run python pipeline.py <any_integer>
```
## 3. Creating a Dockerfile.
  
- In terminal:

```bash
cd pipeline
docker build -t test:pandas .
```
```bash
docker run -it test:pandas < any number >
```

## 4. Running Postgres SQL inside Docker (Bind Mounds).
  
- In terminal:

```bash
cd pipeline

mkdir ny_taxi_postgres_data
docker run -it \
  -e POSTGRES_USER="root" \                           
  -e POSTGRES_PASSWORD="root" \                          
  -e POSTGRES_DB="ny_taxi" \                               
  -v $(pwd)/ny_taxi_postgres_data:/var/lib/postgresql \     
  -p 5432:5432 \
  postgres:18

uv run pip install pgcli
uv run pgcli -h localhost -p 5432 -u root -d ny_taxi
```

  Inside Postgres :

  ```bash
  \dt
  
  CREATE TABLE test (id INTEGER, name VARCHAR(50));
  
  INSERT INTO test VALUES (1, 'vadapav');
  
  SELECT * FROM test;
  
  \q
  ```

If you want to use named volumes instead (managed by docker), run:

```bash
docker run -it --rm \
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="ny_taxi" \
  -v ny_taxi_postgres_data:/var/lib/postgresql \
  -p 5432:5432 \
  postgres:18
```

## 5. Data processing with pandas and data ingestion (chunking).

Refer to `ingestion.py`.  
 
- In terminal:

```bash
cd pipeline
uv run ingestion.py --year 2021 --month <any_month_upto_7>
```
After the ingestion is complete, test the table created:

```bash
uv run pgcli -h localhost -p 5432 -u root -d ny_taxi
```

  Inside Postgres :

  ```bash
  SELECT COUNT(*) FROM yellow_taxi_trips;

  SELECT * FROM yellow_taxi_trips LIMIT 10;

  SELECT 
      DATE(tpep_pickup_datetime) AS pickup_date,
      COUNT(*) AS trips_count,
      AVG(total_amount) AS avg_amount
  FROM yellow_taxi_trips
  GROUP BY DATE(tpep_pickup_datetime)
  ORDER BY pickup_date;
  ```

## 6. Dockerizing and launching multiple containers using docker-compose (.yml) file.

We would run different containers (`pgAdmin` and `Postgres`) on the same virtual docker network.
 
- In terminal:

`docker network create pg-network`

Stop both the containers and re-run them within the same network:

```bash
# run pgsql on the network
docker run -it \
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="ny_taxi" \
  -v ny_taxi_postgres_data:/var/lib/postgresql \
  -p 5432:5432 \
  --network=pg-network \
  --name pgdatabase \
  postgres:18

# in another terminal, run pgAdmin on the same network
docker run -it \
  -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
  -e PGADMIN_DEFAULT_PASSWORD="root" \
  -v pgadmin_data:/var/lib/pgadmin \
  -p 8085:80 \
  --network=pg-network \
  --name pgadmin \
  dpage/pgadmin4
```

Refer to `Dockerfile` for dockerization configurations. 

- In terminal:

```bash
docker build -t ingest_data:v001
```

Run the containerized ingestion:

```bash
docker run -it \
  --network=pg-network \
  taxi_ingest:v001 \
    --pg-user=root \
    --pg-pass=root \
    --pg-host=pgdatabase \
    --pg-port=5432 \
    --pg-db=ny_taxi \
    --target-table=yellow_taxi_data_2021_2 \
    --year=2021 \
    --month=2 \
    --chunksize=100000
```

Multiple containers can be launched simultaneously using `.yml` file.
(Refer to `docker-compose.yml`)

- In terminal:

```bash
docker rm $(docker ps -aq)      # remove all the existing images

docker-compose up

docker network ls               # list all the networks and choose the pipeline network
                                # it is named automatically by docker
                                # e.g. pipeline_pg-network
```
Launch the ingestion container again with the new network name:

```bash
docker run -it --rm \
  --network=pipeline_pg-network \
  taxi_ingest:v001 \
    --pg-user=root \
    --pg-pass=root \
    --pg-host=pgdatabase \
    --pg-port=5432 \
    --pg-db=ny_taxi \
    --target-table=yellow_taxi_data_2021_1 \
    --year=2021 \
    --month=1 \
    --chunksize=100000
```