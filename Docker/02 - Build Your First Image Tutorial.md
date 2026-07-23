# Tutorial: Build Your First Image

## Goal

Package a tiny website as an image.

![[pdf-build-image-container.png]]

Create `index.html`:

```html
<h1>Hello from my Docker image</h1>
```

Create `Dockerfile`:

```Dockerfile
FROM nginx:alpine
COPY index.html /usr/share/nginx/html/index.html
EXPOSE 80
```

Build and run it:

```bash
docker build -t my-site:1.0 .
docker run --rm -p 8080:80 my-site:1.0
```

The final `.` is the build context: files the builder may access. Add `.dockerignore` to keep source control, logs, dependencies, and secrets out of that context:

```gitignore
.git
node_modules
.env
*.log
```

Change the heading, rebuild, and refresh the browser. Images are immutable snapshots, so application changes require a rebuild.
