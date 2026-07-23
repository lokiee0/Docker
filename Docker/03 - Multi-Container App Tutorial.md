# Tutorial: A Multi-Container App with Compose

## Goal

Run PostgreSQL and Adminer together with persistent database storage.

Create `compose.yaml`:

```yaml
services:
  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: app
      POSTGRES_PASSWORD: change-me
      POSTGRES_DB: appdb
    volumes:
      - postgres-data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U app -d appdb"]
      interval: 5s
      timeout: 3s
      retries: 10
  adminer:
    image: adminer:latest
    ports: ["8080:8080"]
    depends_on:
      db:
        condition: service_healthy
volumes:
  postgres-data:
```

```bash
docker compose up -d
docker compose ps
docker compose logs -f
```

Open `http://localhost:8080`. Log in with host `db`, user `app`, password `change-me`, database `appdb`. In a real project put credentials in uncommitted configuration or a secret manager.

Create a table, then run `docker compose down` and `docker compose up -d`. Data remains in the named volume. `docker compose down -v` deletes named volumes; use it only for an intentional reset.
