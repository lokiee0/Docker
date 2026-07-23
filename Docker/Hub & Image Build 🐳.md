

## Docker Hub

Docker Hub is a registry used to:
- Store images
- Pull images
- Push custom images

Official Site:
https://hub.docker.com

---

# Basic Commands

| Purpose | Command |
|---|---|
| Login | `docker login` |
| Logout | `docker logout` |
| Pull image | `docker pull nginx` |
| Push image | `docker push username/image:tag` |
| View images | `docker images` |
| Show digests | `docker images --digests` |
| Inspect image | `docker inspect image_name` |
| Remove image | `docker rmi image_name` |

---

# Image Naming Format

```bash
username/image:tag
```

Example:

```bash
logesh8110874487/myapp:v1
```

---

# Docker Build Workflow

## 1. Create Project

```bash
mkdir myapp
cd myapp
```

---

## 2. Create Dockerfile

```bash
vi Dockerfile
```

### Dockerfile

```dockerfile
FROM nginx

COPY . /usr/share/nginx/html
```

---

## 3. Create HTML File

```bash
echo "Hello Docker" > index.html
```

---

## 4. Build Image

```bash
docker build -t logesh8110874487/myapp:v1 .
```

---

## 5. Verify Image

```bash
docker images
```

---

# Push Image

## Login

```bash
docker login
```

---

## Push

```bash
docker push logesh8110874487/myapp:v1
```

---

## Verify Digest

```bash
docker images --digests
```

---

# Run Container

```bash
docker run -d -p 8080:80 logesh8110874487/myapp:v1
```

---

# Check Running Containers

```bash
docker ps
```

---

# Access Application

```text
http://EC2_PUBLIC_IP:8080
```

---

# Docker Tag

```bash
docker tag nginx logesh8110874487/nginx:v1
```

---

# Docker Inspect

```bash
docker inspect nginx
```

---

# Scratch Image

```dockerfile
FROM scratch
```

Used for:
- Minimal containers
- Static binaries

---

# Common Mistakes

## Wrong

```bash
docker push image
```

## Correct

```bash
docker push username/image:tag
```

---

## Wrong

```bash
docekr images
```

## Correct

```bash
docker images
```

---

# Cleanup

```bash
docker system prune -a
```

---

# Useful Commands

```bash
docker images
docker ps
docker ps -a
docker pull nginx
docker build -t myapp:v1 .
docker push username/myapp:v1
docker inspect nginx
docker logs container_id
docker exec -it container_id bash
docker system df
```

---

# Mental Model

| Component | Meaning |
|---|---|
| Image | Blueprint |
| Container | Running instance |
| Dockerfile | Recipe |
| Docker Hub | Registry |
| Tag | Version |
| Digest | Unique fingerprint |