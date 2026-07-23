# Reference: Docker Commands

## Images

```bash
docker pull nginx:alpine
docker images
docker build -t my-app:1.0 .
docker tag my-app:1.0 registry.example.com/my-app:1.0
docker push registry.example.com/my-app:1.0
docker image rm my-app:1.0
```

## Containers

```bash
docker run --name app -d -p 8080:80 nginx:alpine
docker ps
docker ps -a
docker start app
docker stop app
docker restart app
docker rm app
docker exec -it app sh
docker logs -f --tail 100 app
docker inspect app
```

## Storage, networking, and Compose

```bash
docker volume create app-data
docker volume ls
docker network create app-net
docker network inspect app-net
docker compose config
docker compose up -d --build
docker compose ps
docker compose logs -f SERVICE
docker compose exec SERVICE sh
docker compose down
```

## Cleanup

```bash
docker system df
docker container prune
docker image prune
docker volume prune
docker system prune
```

Review prune commands before running them. Volumes can contain irreplaceable data; `docker system prune -a` removes all unused images.
