# How-to: Troubleshoot Docker Problems

## A container immediately stops

```bash
docker ps -a
docker logs NAME
docker inspect NAME --format '{{.State.ExitCode}}'
```

The command may have completed, crashed, or launched the service in daemon mode. A container stays alive only while its main foreground process runs.

## “Port is already allocated”

Find the existing process/container with `docker ps`, stop it, or select a different host port:

```bash
docker run -p 8081:80 nginx:alpine
```

## Services cannot connect

Ensure both containers share a user-defined network or Compose project. Connect through the service/container name and internal port—not `localhost`.

```bash
docker network inspect NETWORK
docker exec APP getent hosts db
```

## Host changes do not appear

An image is a build-time snapshot. Rebuild and recreate, or use a bind mount for live development:

```bash
docker compose up -d --build
```

## Database data disappeared

Data was in the container layer, or its volume was removed. Use a named volume at the database data path. Avoid `docker compose down -v` unless a reset is intended.

## Builds are slow or disk usage grows

Use `.dockerignore`, order cache-friendly Dockerfile instructions, and inspect usage before cleanup:

```bash
docker system df
docker system prune
```

Review cleanup before confirming it; volumes may contain important data.
