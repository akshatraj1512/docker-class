# docker-class

## 1. Executing Local Scripts inside a Docker Container (Bind Mounts).

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
docker build -t test:pandas .
```
```bash
docker run -it test:pandas < any number >
```
