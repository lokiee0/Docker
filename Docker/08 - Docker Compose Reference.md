# Reference: Docker Compose

Compose declares a multi-container application in `compose.yaml`.

```yaml
services:
  api:
    build: .
    image: example/api:1.0
    ports: ["127.0.0.1:3000:3000"]
    environment:
      LOG_LEVEL: info
    env_file: .env
    volumes:
      - uploads:/app/uploads
    depends_on:
      db:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "wget", "-qO-", "http://localhost:3000/health"]
      interval: 10s
      timeout: 3s
      retries: 3
    restart: unless-stopped
  db:
    image: postgres:16-alpine
    volumes:
      - db-data:/var/lib/postgresql/data
volumes:
  uploads:
  db-data:
```

| Field | Meaning |
| --- | --- |
| `image` | Image to run. |
| `build` | Build configuration/context. |
| `ports` | Host-to-container mappings. |
| `environment` / `env_file` | Runtime configuration. |
| `volumes` | Persistent storage or bind mounts. |
| `depends_on` | Start order; health condition can wait for readiness. |
| `healthcheck` | Command used to assess health. |
| `restart` | Restart policy. |

```bash
docker compose config
docker compose up -d
docker compose up -d --build
docker compose ps
docker compose logs -f
docker compose exec api sh
docker compose down
```

Use `docker compose config` before starting to validate and display resolved configuration.
