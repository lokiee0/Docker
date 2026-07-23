# Tutorial: Docker Fundamentals

## Goal

Run, inspect, enter, stop, and remove a container.

Containerization packages an application and its dependencies into a portable unit. Containers share the host's kernel while isolating their filesystem, processes, and networking, which makes them lighter than virtual machines.

![[pdf-container-vs-vm.png]]

```bash
docker run --name web -d -p 8080:80 nginx:alpine
docker ps
docker logs web
docker exec -it web sh
docker stop web
docker rm web
```

Open `http://localhost:8080` after the first command. `-d` runs in the background; `-p HOST:CONTAINER` publishes a port. `exec` opens a shell inside the running container.

| Term | Meaning |
| --- | --- |
| Image | Immutable package/template. |
| Container | Running or stopped instance of an image. |
| Registry | Image store, such as Docker Hub. |
| Dockerfile | Recipe for building an image. |
| Volume | Docker-managed persistent data. |

Run `docker ps -a` and `docker images`. Stopping/removing a container does not remove its image.
