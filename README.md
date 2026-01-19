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
  -e POSTGRES_DB="ny_taxi" \                                #environment variables
  -v $(pwd)/ny_taxi_postgres_data:/var/lib/postgresql \     #and bind mound
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
  -v ny_taxi_postgres_data:/var/lib/postgresql \   #named volume
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


