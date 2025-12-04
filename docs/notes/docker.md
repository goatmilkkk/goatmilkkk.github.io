# Docker

```python
docker pull python:3.13.8-slim
docker run --name mypython -it python:3.13.8-slim bash
docker cp output.pyc mypython:/home/output.pyc
------------------------------------------------------------------
docker compose up
docker compose up --build
docker compose up --build -t myimage
------------------------------------------------------------------
docker build -t myimage .
docker run --rm -p 1234:80 myimage  # remove when exit
------------------------------------------------------------------
docker ps
docker exec -it <id> /bin/bash
```

## Docker Harbour

```sql
docker run registry/team2/gateway-defense:latest
docker ps
docker cp gateway-server 2d053eb4a0dc:/app
docker exec -it 2d053eb4a0dc /bin/bash
docker commit -m "patch" 2d053eb4a0dc registry/sgscteam2/gateway-defense:latest
docker push registry/team2/gateway-defense:latest
```