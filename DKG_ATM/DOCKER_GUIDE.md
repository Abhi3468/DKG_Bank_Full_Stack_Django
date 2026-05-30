# Docker Setup Guide for ATM Bank

## Quick Start

### 1. **Build and Run Docker Containers**

```bash
# Build the Docker images
docker-compose build

# Start all containers
docker-compose up -d

# Check if containers are running
docker-compose ps
```

### 2. **Access the Application**

- **Web Application**: http://localhost (via Nginx)
- **Direct Django**: http://localhost:8000
- **Database**: postgres://localhost:5432/atm_db

### 3. **Database Setup**

Migrations run automatically, but if needed manually:

```bash
# Run migrations
docker-compose exec web python manage.py migrate

# Create superuser
docker-compose exec web python manage.py createsuperuser

# Collect static files
docker-compose exec web python manage.py collectstatic --noinput
```

### 4. **View Logs**

```bash
# View all logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f web
docker-compose logs -f db
docker-compose logs -f nginx
```

### 5. **Stop Containers**

```bash
# Stop all running containers
docker-compose stop

# Stop and remove containers (keeps volumes)
docker-compose down

# Stop and remove everything including volumes
docker-compose down -v
```

---

## Detailed Commands

### Container Management

```bash
# List all running containers
docker-compose ps

# Execute command in container
docker-compose exec web bash
docker-compose exec db psql -U atm_user -d atm_db

# Rebuild specific service
docker-compose build web

# Restart containers
docker-compose restart

# Rebuild and start
docker-compose up -d --build
```

### Django Management

```bash
# Run shell
docker-compose exec web python manage.py shell

# Create test data
docker-compose exec web python manage.py create_test_data

# Run tests
docker-compose exec web python manage.py test

# Check for issues
docker-compose exec web python manage.py check
```

### Database Operations

```bash
# Access PostgreSQL
docker-compose exec db psql -U atm_user -d atm_db

# Backup database
docker-compose exec db pg_dump -U atm_user -d atm_db > backup.sql

# Restore database
docker-compose exec db psql -U atm_user -d atm_db < backup.sql

# Show database size
docker-compose exec db du -sh /var/lib/postgresql/data/
```

### Debugging

```bash
# Check web container logs
docker-compose logs web --tail=50

# Check database connection
docker-compose exec web python -c "import django; django.setup(); from django.db import connection; print(connection.ensure_connection())"

# Check static files
docker-compose exec web ls -la staticfiles/

# Verify environment variables
docker-compose exec web env | grep DATABASE
```

---

## Architecture

```
┌─────────────────────────────────────────┐
│         Docker Compose Stack            │
├─────────────────────────────────────────┤
│                                         │
│  ┌─────────────────────────────────┐   │
│  │      Nginx (Port 80)            │   │
│  │  - Serves static files          │   │
│  │  - Proxies to Django            │   │
│  │  - Handles SSL (optional)       │   │
│  └────────────┬────────────────────┘   │
│               │                         │
│  ┌────────────▼────────────────────┐   │
│  │  Django/Gunicorn (Port 8000)    │   │
│  │  - Application logic            │   │
│  │  - 4 worker processes           │   │
│  │  - WhiteNoise middleware        │   │
│  └────────────┬────────────────────┘   │
│               │                         │
│  ┌────────────▼────────────────────┐   │
│  │   PostgreSQL (Port 5432)        │   │
│  │   - Database: atm_db            │   │
│  │   - Persistent volume           │   │
│  └─────────────────────────────────┘   │
│                                         │
└─────────────────────────────────────────┘
```

---

## Environment Variables

Create `.env` file from `.env.docker`:

```bash
# Copy the template
cp .env.docker .env

# Edit with your values
nano .env
```

Key variables:
- `DEBUG`: Set to `False` in production
- `SECRET_KEY`: Generate a strong key for production
- `DATABASE_URL`: PostgreSQL connection string
- `ALLOWED_HOSTS`: Comma-separated list of allowed hosts
- `EMAIL_HOST`: SMTP server for sending emails

---

## Production Checklist

Before deploying to production:

- [ ] Set `DEBUG=False`
- [ ] Generate a strong `SECRET_KEY`
- [ ] Update `ALLOWED_HOSTS` with your domain
- [ ] Set up SSL/TLS certificates in Nginx
- [ ] Configure email settings
- [ ] Set up backup strategy for database
- [ ] Configure log rotation
- [ ] Set up monitoring and alerts
- [ ] Update security headers in Nginx
- [ ] Use strong database password

---

## Troubleshooting

### Ports Already in Use

```bash
# Find process using port
lsof -i :8000
lsof -i :5432
lsof -i :80

# Kill process
kill -9 <PID>

# Or use different port in docker-compose.yml
```

### Static Files Not Loading

```bash
# Collect static files again
docker-compose exec web python manage.py collectstatic --noinput --clear

# Check static volume
docker volume ls | grep static

# Restart Nginx
docker-compose restart nginx
```

### Database Connection Issues

```bash
# Check database is running
docker-compose ps db

# View database logs
docker-compose logs db

# Test connection from web container
docker-compose exec web psql -h db -U atm_user -d atm_db -c "SELECT 1;"
```

### Permission Denied Issues

```bash
# Fix file permissions
docker-compose exec web chown -R appuser:appuser /app

# Or run as root temporarily
docker-compose exec -u root web chown -R appuser:appuser /app
```

---

## Performance Tips

1. **Database**: Add indexes for frequently queried fields
2. **Caching**: Enable Redis for session/cache storage
3. **Static Files**: Use CDN for serving static files
4. **Worker Processes**: Adjust `workers` in Dockerfile based on CPU cores
5. **Database Connections**: Pool connections with PgBouncer

---

## Useful Links

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Django Deployment Checklist](https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/)
- [Gunicorn Configuration](https://docs.gunicorn.org/en/latest/settings.html)
- [Nginx Documentation](https://nginx.org/en/docs/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
