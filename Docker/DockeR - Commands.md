

# 🐳 Docker — Part 2 : Commands Reference

> All Docker commands in one place. Use this as your daily reference.

---

## 📑 Table of Contents

- [[#System & Info]]
- [[#Images]]
- [[#Containers — Basic]]
- [[#Containers — Control]]
- [[#Containers — Inspect & Debug]]
- [[#Port Mapping]]
- [[#Volumes]]
- [[#Networking]]
- [[#Cleanup]]
- [[#Docker Compose]]
- [[#Quick Cheat Sheet]]

---

## System & Info

|Command|Purpose|
|---|---|
|`docker --version`|Check Docker version|
|`docker info`|Display full Docker system info|
|`docker help`|Show help for all commands|
|`docker system df`|Show Docker disk usage|

---

## Images

|Command|Purpose|
|---|---|
|`docker pull nginx`|Download image from Docker Hub|
|`docker images`|List all local images|
|`docker search nginx`|Search images on Docker Hub|
|`docker rmi IMAGE_NAME`|Remove/delete an image|
|`docker image prune`|Remove all unused images|
|`docker build -t name:tag .`|Build image from Dockerfile|
|`docker push repo/image`|Push image to registry|

---

## Containers — Basic

|Command|Purpose|
|---|---|
|`docker run nginx`|Run a container|
|`docker run -d nginx`|Run in background (detached)|
|`docker run -it ubuntu bash`|Run interactively with terminal|
|`docker run --name my-app nginx`|Run with a custom name|
|`docker run -d -p 8080:80 nginx`|Run with port mapping|
|`docker ps`|Show running containers|
|`docker ps -a`|Show all containers (including stopped)|

---

## Containers — Control

|Command|Purpose|
|---|---|
|`docker stop CONTAINER_ID`|Gracefully stop a container|
|`docker start CONTAINER_ID`|Start a stopped container|
|`docker restart CONTAINER_ID`|Restart a container|
|`docker kill CONTAINER_ID`|Force stop a container|
|`docker pause CONTAINER_ID`|Pause a container|
|`docker unpause CONTAINER_ID`|Resume a paused container|
|`docker rm CONTAINER_ID`|Remove a stopped container|
|`docker rm -f CONTAINER_ID`|Force remove a running container|
|`docker rename oldname newname`|Rename a container|

---

## Containers — Inspect & Debug

|Command|Purpose|
|---|---|
|`docker logs CONTAINER_ID`|View container logs|
|`docker logs -f CONTAINER_ID`|Follow logs in real time|
|`docker exec -it CONTAINER_ID bash`|Open a shell inside the container|
|`docker inspect CONTAINER_ID`|Detailed info (JSON format)|
|`docker top CONTAINER_ID`|Show running processes inside|
|`docker stats`|Live CPU & RAM usage of all containers|
|`docker cp file.txt CONTAINER_ID:/tmp`|Copy a file into a container|

---

## Port Mapping

```bash
docker run -d -p 8080:80 nginx
```

```
Your PC : 8080  →  Container : 80
```

Open in browser → **http://localhost:8080**

|Example|Meaning|
|---|---|
|`-p 8080:80`|PC port 8080 → container port 80|
|`-p 3000:3000`|PC port 3000 → container port 3000|
|`-p 5432:5432`|PC port 5432 → Postgres default port|

---

## Volumes

> Keeps data alive even after a container is removed.

|Command|Purpose|
|---|---|
|`docker volume create my-data`|Create a named volume|
|`docker volume ls`|List all volumes|
|`docker volume rm my-data`|Remove a volume|
|`docker volume prune`|Remove all unused volumes|

```bash
# Attach a named volume when running
docker run -d -v my-data:/app/data my-app

# Bind mount — sync local folder with container
docker run -d -v $(pwd)/data:/app/data my-app
```

---

## Networking

|Command|Purpose|
|---|---|
|`docker network ls`|List all Docker networks|
|`docker network create my-net`|Create a custom network|
|`docker network rm my-net`|Remove a network|
|`docker network inspect my-net`|Inspect network details|

```bash
# Connect two containers on the same network
docker run -d --network my-net --name app  my-app
docker run -d --network my-net --name db   postgres

# Now "app" can reach "db" just by using the name "db"
```

---

## Cleanup

|Command|Purpose|
|---|---|
|`docker container prune`|Remove all stopped containers|
|`docker image prune`|Remove unused images|
|`docker volume prune`|Remove unused volumes|
|`docker system prune`|Remove ALL unused data|
|`docker system df`|Check how much disk Docker uses|

> ⚠️ `docker system prune` removes containers, images, networks & build cache. Use with care.

---

## Docker Compose

|Command|Purpose|
|---|---|
|`docker compose up -d`|Start all services in background|
|`docker compose down`|Stop and remove all services|
|`docker compose ps`|List running services|
|`docker compose logs -f`|Follow logs for all services|
|`docker compose build`|Build/rebuild images|
|`docker compose up -d --build`|Rebuild and restart|
|`docker compose restart`|Restart all services|
|`docker compose exec web bash`|Shell into a specific service|

---

## ⚡ Quick Cheat Sheet

```bash
# ── Images ──────────────────────────────────────────
docker pull <image>            # Download image
docker images                  # List images
docker rmi <image>             # Delete image
docker build -t name:tag .     # Build from Dockerfile

# ── Run Container ───────────────────────────────────
docker run <image>             # Basic run
docker run -d <image>          # Background (detached)
docker run -it <image> bash    # Interactive shell
docker run -d -p 8080:80 \
  --name myapp <image>         # Full run command

# ── Manage Containers ───────────────────────────────
docker ps                      # Running containers
docker ps -a                   # All containers
docker stop <name/id>          # Stop
docker start <name/id>         # Start
docker rm <name/id>            # Delete
docker rm -f <name/id>         # Force delete

# ── Debug ────────────────────────────────────────────
docker logs -f <name>          # Follow logs
docker exec -it <name> bash    # Open shell
docker stats                   # CPU / RAM live view
docker inspect <name>          # Full JSON details

# ── Compose ─────────────────────────────────────────
docker compose up -d           # Start all
docker compose down            # Stop all
docker compose logs -f         # Watch all logs
docker compose up -d --build   # Rebuild & start

# ── Cleanup ─────────────────────────────────────────
docker system prune            # Clean everything unused
docker container prune         # Clean stopped containers
docker image prune             # Clean unused images
```

---

_Tags: #docker #devops #commands #reference_