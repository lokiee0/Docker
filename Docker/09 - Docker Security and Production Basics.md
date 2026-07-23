# How-to: Prepare a Dockerized App for Production

## Checklist

- Use a maintained, versioned base image and rebuild regularly.
- Build a small runtime image with multi-stage builds.
- Run the application as a non-root user.
- Do not bake `.env`, private keys, tokens, or credentials into image layers.
- Use explicit image tags and record image digests for deployments when possible.
- Add a meaningful health check; configure CPU and memory limits in deployment.
- Write logs to standard output/error.
- Persist state outside the disposable container layer.
- Bind development-only ports to `127.0.0.1` where appropriate.

```Dockerfile
FROM node:22-alpine AS build
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM node:22-alpine
WORKDIR /app
ENV NODE_ENV=production
COPY package*.json ./
RUN npm ci --omit=dev
COPY --from=build /app/dist ./dist
USER node
EXPOSE 3000
CMD ["node", "dist/server.js"]
```

Test the non-root image locally. If it needs a writable directory, set that directory’s ownership during the build rather than returning to root at runtime.
