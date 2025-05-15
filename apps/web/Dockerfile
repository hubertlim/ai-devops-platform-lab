# =============================================================================
# Frontend Web - Multi-stage Dockerfile
# =============================================================================

# ---------------------------------------------------------------------------
# Base stage: install dependencies
# ---------------------------------------------------------------------------
FROM node:20-alpine AS base

WORKDIR /app

COPY package.json package-lock.json* ./
RUN npm ci

# ---------------------------------------------------------------------------
# Development stage: Vite dev server with HMR
# ---------------------------------------------------------------------------
FROM base AS development

COPY . .

EXPOSE 5173

CMD ["npm", "run", "dev"]

# ---------------------------------------------------------------------------
# Build stage: compile TypeScript and bundle
# ---------------------------------------------------------------------------
FROM base AS build

COPY . .
RUN npm run build

# ---------------------------------------------------------------------------
# Production stage: serve static files with nginx
# ---------------------------------------------------------------------------
FROM nginx:1.25-alpine AS production

RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
