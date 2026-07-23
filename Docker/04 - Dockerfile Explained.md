# Explanation: Dockerfiles and Image Builds

A Dockerfile describes how Docker constructs an image. Instructions usually create cached layers, so put stable work first and frequently changing source code later.

## Create, build, and run

```bash
mkdir hello-docker && cd hello-docker
touch Dockerfile .dockerignore
# Edit Dockerfile, then:
docker build -t hello-docker:1.0 .
docker run --rm -p 8080:80 hello-docker:1.0
```

Use another filename with `docker build -f Dockerfile.dev -t hello-docker:dev .`. `docker image inspect hello-docker:1.0` shows the image configuration.

## Dockerfile instruction reference

| Instruction   | Example                                                            | Use                                                                         |         |                                           |
| ------------- | ------------------------------------------------------------------ | --------------------------------------------------------------------------- | ------- | ----------------------------------------- |
| `FROM`        | `FROM node:22-alpine`                                              | Choose a base image.                                                        |         |                                           |
| `ARG`         | `ARG VERSION=1.0`                                                  | Build-time variable; not retained at runtime.                               |         |                                           |
| `RUN`         | `RUN npm ci`                                                       | Execute a command while building.                                           |         |                                           |
| `COPY`        | `COPY package*.json ./`                                            | Copy files from the build context.                                          |         |                                           |
| `ADD`         | `ADD archive.tar.gz /app/`                                         | Copy and automatically unpack a local tar archive; prefer `COPY` otherwise. |         |                                           |
| `WORKDIR`     | `WORKDIR /app`                                                     | Set the working directory for later instructions.                           |         |                                           |
| `ENV`         | `ENV NODE_ENV=production`                                          | Set a runtime default environment variable.                                 |         |                                           |
| `EXPOSE`      | `EXPOSE 3000`                                                      | Document a listening port; it does not publish it.                          |         |                                           |
| `USER`        | `USER node`                                                        | Set the user for later `RUN` commands and the container.                    |         |                                           |
| `VOLUME`      | `VOLUME ["/data"]`                                                 | Declare a mount point for persistent data.                                  |         |                                           |
| `LABEL`       | `LABEL org.opencontainers.image.source="https://example.com/repo"` | Add image metadata.                                                         |         |                                           |
| `HEALTHCHECK` | `HEALTHCHECK CMD wget -qO- http://localhost:3000/health            |                                                                             | exit 1` | Tell Docker how to test container health. |
| `STOPSIGNAL`  | `STOPSIGNAL SIGTERM`                                               | Choose the signal sent when the container stops.                            |         |                                           |
| `SHELL`       | `SHELL ["/bin/bash", "-c"]`                                        | Change the shell form interpreter.                                          |         |                                           |
| `ONBUILD`     | `ONBUILD COPY . /src`                                              | Add a trigger for child images; use sparingly.                              |         |                                           |
| `CMD`         | `CMD ["node", "server.js"]`                                        | Set the default command or arguments.                                       |         |                                           |
| `ENTRYPOINT`  | `ENTRYPOINT ["node"]`                                              | Set the fixed executable.                                                   |         |                                           |

`MAINTAINER` is obsolete; use `LABEL` instead. Use JSON/exec form (`["command", "arg"]`) for `CMD` and `ENTRYPOINT` so Docker sends signals directly to the application.

```Dockerfile
FROM node:22-alpine AS build
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
USER nginx
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

Copy dependency manifests before source to reuse the dependency layer. Multi-stage builds keep compilers and source dependencies out of the runtime image. Prefer versioned bases, `.dockerignore`, JSON-form commands, and non-root users. Never put secrets in the build context or image.

## `CMD` and `ENTRYPOINT`

`ENTRYPOINT` fixes the executable; `CMD` supplies its default arguments. Runtime arguments replace `CMD` values:

```Dockerfile
FROM alpine:3.21
ENTRYPOINT ["sleep"]
CMD ["3600"]
```

`docker run image 1800` runs `sleep 1800`. A container exits when its foreground process exits.
