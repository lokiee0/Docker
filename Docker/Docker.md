# 🐳 Docker —  Concepts & How It Works

> **What is Docker?** A platform to **package, ship, and run** apps inside lightweight isolated environments called **containers**.

---

## 📑 Table of Contents

- [[#What Problem Does Docker Solve?]]
- [[#Core Concepts]]
- [[#Docker Architecture]]
- [[#Image vs Container]]
- [[#Dockerfile]]
- [[#Docker Compose]]
- [[#Volumes & Networking]]
- [[#Docker vs Virtual Machine]]
- [[#Real-World Workflow]]
- [[#Learning Order]]

---

## What Problem Does Docker Solve?

> _"It works on my machine!"_ — Every developer, ever.

Without Docker, apps break because of:

- Different OS versions across machines
- Missing dependencies
- Conflicting library versions

Docker fixes this by bundling your app **with everything it needs** into one container.

```
Your App
  + Code
  + Runtime  (Node, Python, Java…)
  + Libraries & Dependencies
  + Config
────────────────────────────────
= 📦 One Container → Runs Anywhere
```

---

## Core Concepts

### 🖼️ Image

- A **read-only blueprint/template** for a container
- Like a **class** in OOP — defined once, used many times
- Built from a `Dockerfile`
- Examples: `ubuntu`, `nginx`, `mysql`, `node:18`

> How image layers stack up — each instruction in a Dockerfile adds a layer:

![[docker-image-layers.png]]

> How the thin read/write container layer sits on top of read-only image layers:

![[docker-container-layers.jpg]]

---

### 📦 Container

- A **running instance** of an image
- Like an **object** created from a class
- Isolated, lightweight, disposable
- Many containers can run from one image

> Multiple containers sharing the same base image layers (saves disk space):

![[docker-sharing-layers.jpg]]

> The writeable layer added on top when a container runs:

![[docker-container-writeable-layer.png]]

---

### 🏪 Docker Hub / Registry

- A cloud store for sharing images
- Like **GitHub, but for Docker images**
- → [hub.docker.com](https://hub.docker.com/)

> Full workflow — build locally, push to registry, pull on any server:

![[docker-registry-hub-workflow.png]]

---

## Docker Architecture

```
┌─────────────────────────────────────────┐
│            Docker Client (YOU)          │
│         types: docker run nginx         │
└──────────────────┬──────────────────────┘
                   │  REST API
┌──────────────────▼──────────────────────┐
│           Docker Daemon (Engine)        │
│                                         │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐ │
│  │Container│  │Container│  │Container│ │
│  └─────────┘  └─────────┘  └─────────┘ │
└─────────────────────────────────────────┘
                   │
       ┌───────────▼──────────┐
       │   Docker Registry    │
       │    (Docker Hub)      │
       └──────────────────────┘
```

> Visual overview of the full Docker architecture (Client → Daemon → Registry):

![[docker-architecture.png]]

|Component|Role|
|---|---|
|**Client**|The CLI you type commands into|
|**Daemon**|Background engine that manages containers|
|**Registry**|Remote store where images live|

---

## Image vs Container

> Side-by-side comparison — what's an Image vs what's a Container:

![[docker-image-vs-container.png]]

| | Image | Container |
|---|---|---|
|What it is|Blueprint (read-only)|Running instance|
|Created by|`docker build`|`docker run`|
|Stored in|Registry / local|Your machine (running)|
|Lifespan|Permanent until deleted|Temporary / disposable|

---

## Dockerfile

Defines how to **build your own image**, step by step.

### Structure & Example

```dockerfile
# 1. Start from a base image
FROM node:18-alpine

# 2. Set working directory inside container
WORKDIR /app

# 3. Copy dependency file first (for caching)
COPY package*.json ./

# 4. Install dependencies
RUN npm install

# 5. Copy your source code
COPY . .

# 6. Tell Docker which port the app uses
EXPOSE 3000

# 7. Command to run when container starts
CMD ["node", "server.js"]
```

### Key Instructions

|Instruction|What It Does|Example|
|---|---|---|
|`FROM`|Base image to build on|`FROM python:3.11`|
|`WORKDIR`|Set working directory|`WORKDIR /app`|
|`COPY`|Copy files into image|`COPY . .`|
|`RUN`|Run command during build|`RUN npm install`|
|`CMD`|Command on container start|`CMD ["python", "app.py"]`|
|`EXPOSE`|Document the app's port|`EXPOSE 8080`|
|`ENV`|Set environment variables|`ENV NODE_ENV=production`|

### Build & Run

```bash
# Build image from Dockerfile
docker build -t my-app:1.0 .

# Run your image
docker run -d -p 3000:3000 my-app:1.0
```

---

## Docker Compose

Used when your app needs **multiple services together** (web + db + cache).

> How Docker Swarm/Compose scales services across nodes with replicas:

![[docker-swarm-replicas.png]]

### Example: Web App + Database + Cache

```yaml
version: '3.8'

services:

  web:
    build: .
    ports:
      - "3000:3000"
    depends_on:
      - db

  db:
    image: postgres:15
    environment:
      POSTGRES_USER: admin
      POSTGRES_PASSWORD: secret
      POSTGRES_DB: myapp
    volumes:
      - db-data:/var/lib/postgresql/data

  cache:
    image: redis:alpine

volumes:
  db-data:
```

### Compose Commands

```bash
docker compose up -d          # Start all services
docker compose down           # Stop all services
docker compose logs -f        # Watch all logs
docker compose up -d --build  # Rebuild & start
```

---

## Volumes & Networking

### 📁 Volumes — Persisting Data

> Containers are **ephemeral** — all data is lost when removed. Volumes fix this.

> How volumes persist data across multiple containers:

![[docker-volumes-overview.png]]

```bash
docker volume create my-data                    # Create volume
docker run -d -v my-data:/app/data my-app       # Attach volume
docker run -d -v $(pwd)/data:/app/data my-app   # Or bind local folder
```

### 🌐 Networking

```bash
docker network create my-network

# Both containers can talk to each other by name
docker run -d --network my-network --name app my-app
docker run -d --network my-network --name db  postgres
```

> Containers on the **same network** reach each other using their **container name** as the hostname.

---

## Docker vs Virtual Machine

> Docker containers share the host OS kernel — VMs run a full guest OS. This makes containers much lighter and faster:

![[docker-vs-vm.png]]

| | Docker Container | Virtual Machine |
|---|---|---|
|OS|Shares host OS kernel|Full guest OS|
|Startup|Seconds|Minutes|
|Size|Lightweight (MBs)|Heavy (GBs)|
|Performance|Near native|Slower (overhead)|

---

## Real-World Workflow

> Push/pull workflow — from local build to any server:

![[docker-registry-workflow.png]]

```
1. Write your app code
          ↓
2. Write a Dockerfile
          ↓
3. docker build -t myapp .         ← Build image
          ↓
4. docker run -p 8080:3000 myapp   ← Run container
          ↓
5. Test → http://localhost:8080
          ↓
6. docker push myrepo/myapp        ← Push to registry
          ↓
7. On any server → docker pull + docker run ✅
```


---

## 🧪 Beginner Practice

```bash
# Run nginx web server
docker run -d -p 8080:80 nginx
```



---

