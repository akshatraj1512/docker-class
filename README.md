# docker-class

Executing Local Scripts inside a Docker Container (Bind Mounts).

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




