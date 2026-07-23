# How-to: Common Docker Tasks

## Diagnose an exited container

```bash
docker ps -a
docker logs CONTAINER
docker inspect CONTAINER --format '{{.State.ExitCode}}'
```

Read logs first. An exit code of `0` can mean the main command completed; service containers need a foreground process.

## Open a shell or copy files

```bash
docker exec -it CONTAINER sh
docker cp ./local.txt CONTAINER:/tmp/local.txt
docker cp CONTAINER:/tmp/report.txt ./report.txt
```

Use `sh` for minimal images; Bash is often absent.

## Rebuild one Compose service

```bash
docker compose up -d --build SERVICE
docker compose logs -f SERVICE
```

## Pass configuration at runtime

```bash
docker run --rm --env-file .env my-app:1.0
```

Keep `.env` out of Git. For production credentials, use the deployment platform’s secret mechanism.

Environment variables keep configuration out of the image and can control values such as log level, feature flags, and runtime environment. Use `ENV` in a Dockerfile only for safe defaults; use `-e`, `--env-file`, Compose `environment`, or a deployment secret mechanism for environment-specific values and credentials.

## Publish an image

```bash
docker login
docker tag my-app:1.0 YOUR_USER/my-app:1.0
docker push YOUR_USER/my-app:1.0
```

Use version or commit-based tags, not only `latest`.

![[docker-registry-workflow.png]]
