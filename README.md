# Eclipse Labs Metrics API

A secure, production-ready metrics collection and analytics API built with FastAPI.

## Features

- 🔐 Secure authentication with API keys
- 📊 High-performance metrics storage with ClickHouse
- ⚡ Rate limiting with Redis sliding window algorithm
- 🛡️ Comprehensive security hardening
- 🐳 Dockerized for easy deployment
- 📈 RESTful API for metrics ingestion and retrieval

## Security Features

- SQL injection prevention through parameterized queries
- Timing attack protection with constant-time comparisons
- Rate limiting to prevent abuse
- Input validation and sanitization
- Container security (non-root user, minimal privileges)
- Transport encryption (SSL/TLS for databases)
- No sensitive data logging

## Setup Guide

### Prerequisites

- Docker and Docker Compose
- Python 3.12+ (for local development)
- Git

### Environment Variables

The following environment variables must be configured in a `.env` file at the project root:

#### Required Secrets

| Variable | Description | Example |
|----------|-------------|---------|
| `API_KEY` | Primary API key for service authentication | `egos_abcd1234.XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX` |
| `ADMIN_API_KEY` | Admin API key for accessing metrics endpoints | `your-secure-admin-key-here` |
| `RCON_PASSWORD` | RCON password for game server queries | `your-rcon-password` |
| `POSTGRES_PASSWORD` | PostgreSQL database password | `secure-postgres-password` |
| `CLICKHOUSE_PASSWORD` | ClickHouse database password | `secure-clickhouse-password` |
| `REDIS_PASSWORD` | Redis password (required in production) | `secure-redis-password` |

#### Database Configuration

| Variable | Description | Default |
|----------|-------------|---------|
| `POSTGRES_USER` | PostgreSQL username | `postgres` |
| `POSTGRES_HOST` | PostgreSQL host | `localhost` |
| `POSTGRES_PORT` | PostgreSQL port | `5432` |
| `POSTGRES_DB` | PostgreSQL database name | `egos` |
| `CLICKHOUSE_HOST` | ClickHouse host | `localhost` |
| `CLICKHOUSE_PORT` | ClickHouse port | `8123` |
| `CLICKHOUSE_USER` | ClickHouse username | `default` |
| `CLICKHOUSE_DB` | ClickHouse database name | `metrics` |
| `REDIS_HOST` | Redis host | `localhost` |
| `REDIS_PORT` | Redis port | `6379` |

#### Application Configuration

| Variable | Description | Values |
|----------|-------------|--------|
| `ENVIRONMENT` | Application environment | `DEV` or `PROD` |

### Setup Instructions

#### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/metrics-api.git
cd metrics-api
```

#### 2. Create Environment File

Create a `.env` file in the project root with the required variables:

```bash
# Copy the example if available, otherwise create manually
cp .env.example .env  # If .env.example exists
# Or create .env manually with the variables above
```

#### 3. Generate Secure API Keys (Optional but Recommended)

You can generate secure API keys using the provided utility:

```bash
python -c "
import secrets
prefix = secrets.token_hex(4)  # 8 hex chars
secret = secrets.token_urlsafe(32)
full_key = f'egos_{prefix}.{secret}'
print(f'Generated API key: {full_key}')
print(f'Use this for API_KEY: {full_key}')
print(f'Use this for ADMIN_APIKEY: {secrets.token_urlsafe(32)}')
"
```

#### 4. Start the Application

Using Docker Compose (recommended for production):

```bash
docker-compose up -d
```

For development with hot reload:

```bash
# Install dependencies
pip install -e .

# Run the API
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

#### 5. Verify Installation

Check that the API is running:

```bash
curl http://localhost:8000/health
# Should return: {"status":"healthy"}

# Access interactive docs (only in DEV environment)
# Visit: http://localhost:8000/docs
```

### Configuration Notes

#### Environment-Specific Behavior

- **Development (`ENVIRONMENT=DEV`)**:
  - Uses SQLite database for simplicity
  - Enables API documentation at `/docs` and `/redoc`
  - Relaxes some security constraints for easier development

- **Production (`ENVIRONMENT=PROD`)**:
  - Requires all production secrets to be set
  - Uses PostgreSQL with SSL enforcement
  - Uses ClickHouse with HTTPS enforcement
  - Requires REDIS_PASSWORD to be set
  - Disables API documentation to prevent information leakage
  - Enforces stricter security controls

#### Security Notes

1. **Never commit `.env` files** to version control
2. Use strong, randomly generated passwords and keys
3. Rotate credentials regularly
4. Monitor logs for authentication failures
5. Keep dependencies updated

### API Endpoints

#### Metrics Collection
- `POST /event` - Ingest a new metrics event (requires API key)

#### Metrics Retrieval (Admin Only)
- `GET /events` - Retrieve events with filtering and pagination
- `GET /events/count` - Get count of events matching criteria

#### Health Checks
- `GET /health` - Basic health check endpoint
- `GET /metrics` - Prometheus-style metrics (if enabled)

### Docker Compose Services

The `docker-compose.yml` file includes:
- `api`: The FastAPI application
- `postgres`: PostgreSQL database for service metadata
- `clickhouse`: Column-oriented database for metrics storage
- `redis`: In-memory store for rate limiting and caching

### Maintenance

#### Database Migrations

If you modify the PostgreSQL schema, you'll need to run migrations:

```bash
# Generate migration revision
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head
```

#### Logs

View container logs:

```bash
docker-compose logs -f api
docker-compose logs -f postgres
docker-compose logs -f clickhouse
docker-compose logs -f redis
```

### Troubleshooting

#### Common Issues

1. **Connection refused errors**:
   - Ensure all Docker containers are running: `docker-compose ps`
   - Check container logs for startup errors

2. **Authentication failures**:
   - Verify API keys match between client and server
   - Check that `ADMIN_API_KEY` is set for admin endpoints

3. **Database connection issues**:
   - Verify database credentials in `.env`
   - Ensure containers can reach each other on Docker network

4. **Rate limiting too restrictive**:
   - Adjust `RATE_LIMIT_DEFAULT`, `RATE_LIMIT_WINDOW`, or `RATE_LIMIT_BLOCK_AFTER` in config
   - Ensure Redis is running and accessible

### Support

For issues, questions, or contributions, please open an issue on the GitHub repository.

---

**Security Notice**: This API implements security best practices, but you should still:
- Regularly update dependencies
- Monitor security advisories for used technologies
- Conduct periodic security reviews
- Follow the principle of least privilege for API keys