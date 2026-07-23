# Explanation: Docker Storage and Networking

Container writable layers are disposable. Use storage designed to survive container replacement.

![[docker-volumes-overview.png]]

| Type | Best for | Example |
| --- | --- | --- |
| Named volume | Database/application state | `-v pgdata:/var/lib/postgresql/data` |
| Bind mount | Local development files | `-v "$PWD":/app` |
| tmpfs | Temporary in-memory files | `--tmpfs /tmp` |

Named volumes are normally best for databases. Bind mounts connect a container to a host path, useful locally but less portable.

Docker networks allow private service communication. On a user-defined network, names resolve through Docker DNS:

```bash
docker network create app-net
docker run -d --name db --network app-net postgres:16-alpine
docker run --rm --network app-net alpine getent hosts db
```

Publish a port only when the host needs access:

```bash
docker run -p 127.0.0.1:8080:80 nginx:alpine
```

Compose creates a project network automatically. Services reach one another by service name and internal port. `localhost` inside a container means that same container.
