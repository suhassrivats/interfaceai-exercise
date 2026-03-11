FROM postgres:16-alpine

# Copy init script - runs automatically on first container start
COPY init.sql /docker-entrypoint-initdb.d/01-init.sql

# Healthcheck for docker-compose
HEALTHCHECK --interval=5s --timeout=5s --retries=5 \
  CMD pg_isready -U postgres || exit 1
