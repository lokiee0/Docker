# Docker Interview Questions and Practice Labs

## Core questions

### Image versus container?

An image is an immutable packaged template. A container is a running or stopped instance with runtime configuration and a writable layer.

### `CMD` versus `ENTRYPOINT`?

`CMD` provides default command or arguments and is easy to override. `ENTRYPOINT` defines the primary executable. They can be combined.

### Why multi-stage builds?

They separate build tools from the final runtime image, reducing size and attack surface.

### Volume versus bind mount?

A volume is Docker-managed persistent storage. A bind mount exposes a specific host path, usually for local development.

### `EXPOSE` versus `-p`?

`EXPOSE` documents an image port. `-p` publishes a container port to the host.

## Practice labs

1. Run Nginx on port 8080; inspect logs, open a shell, and remove it.
2. Package an `index.html` with `nginx:alpine` and add `.dockerignore`.
3. Run PostgreSQL with a named volume; create data, recreate the container, and verify persistence.
4. Use Compose for PostgreSQL and Adminer; connect using service name `db` without publishing port 5432.
5. Intentionally map two containers to the same host port; diagnose and fix the collision.
6. Improve an earlier Dockerfile with a non-root user, a versioned base, a multi-stage build where useful, and a health check.

For each lab, write down the command, expected result, and what you learned from any failure. That is the fastest route from memorising commands to understanding Docker.
