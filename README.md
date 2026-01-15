# docker-class

## 1. Executing Local Scripts inside a Docker Container (Named Volumes).

- Prerequisites:

  `Python` and `Docker` installed and running.
  
- In terminal:

```bash
docker run -it --entrypoint=bash -v $(pwd)/test:/app/test python:3.13.1-slim
```
```bash
cd /app/test
```
```bash
python script.py
```

## 2. Performing ETL with a simple pipeline 

- Prerequisites:

  Find in the `.toml` file.
  
- In terminal:

```bash
cd /pipeline
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

## 3. Running Postgres SQL inside Docker (Bind Mounds).
  
- In terminal:

```bash
cd pipeline
uv run pip install pgcli
uv run pgcli -h localhost -p 5432 -u root -d ny_taxi
```

  Inside Postgres :

  ```bash
  \dt
  -- List tables
\dt

CREATE TABLE test (id INTEGER, name VARCHAR(50));

INSERT INTO test VALUES (1, 'vadapav');

SELECT * FROM test;

\q
  ```