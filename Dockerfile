# docker-compose.yml
version: '3.8'

services:
  postgres:
    image: postgres:15-alpine
    container_name: mobile_shop_db
    environment:
      POSTGRES_DB: mobi_db
      POSTGRES_USER: mobiadmin
      POSTGRES_PASSWORD: 1234
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql
    ports:
      - "5432:5432"
    restart: unless-stopped
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U mobiadmin -d mobi_db"]
      interval: 10s
      timeout: 5s
      retries: 5

  bot:
    build: .
    container_name: mobile_shop_bot
    environment:
      - BOT_TOKEN=${BOT_TOKEN}
      - DATABASE_URL=postgresql+psycopg2://mobiadmin:1234@postgres:5432/mobi_db
    depends_on:
      postgres:
        condition: service_healthy
    restart: unless-stopped
    volumes:
      - ./app:/app/app:ro
      - ./bot.py:/app/bot.py:ro
      - ./config.py:/app/config.py:ro
      - ./.env:/app/.env:ro

volumes:
  postgres_data:

---
# Dockerfile
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user
RUN adduser --disabled-password --gecos '' botuser && \
    chown -R botuser:botuser /app
USER botuser

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('https://api.telegram.org/bot${BOT_TOKEN}/getMe')" || exit 1

# Run the bot
CMD ["python", "bot.py"]

---
# init.sql
-- This file will be executed when the PostgreSQL container starts
-- Create the database and user (if they don't exist)

-- The database and user are already created by environment variables
-- This file can be used for additional initialization if needed

-- Create extensions if needed
-- CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- You can add any additional SQL initialization here
-- For example, creating indexes or inserting initial data

-- Example: Create an index on frequently queried columns
-- CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_users_telegram_id ON users(telegram_id);
-- CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_products_category_active ON products(category_id, is_active);

GRANT ALL PRIVILEGES ON DATABASE mobi_db TO mobiadmin;