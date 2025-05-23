# =============================================================================
# Frontend Web - Multi-stage Dockerfile
# =============================================================================

# ---------------------------------------------------------------------------
# Base stage: install dependencies
# ---------------------------------------------------------------------------
FROM node:20-alpine@sha256:afdf98210b07b586eb71fa22ba2e432e058e4cd1304d31ed60888755b8c865fb AS base

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
FROM nginx:1.25-alpine@sha256:721fa00bc549df26b3e67cc558ff176112d4ba69847537766f3c28e171d180e7 AS production

RUN apk add --no-cache curl

RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 80

HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD curl --fail --silent http://localhost/nginx-health || exit 1

CMD ["nginx", "-g", "daemon off;"]
