# Docker Quick Reference - ATM Bank

## 🚀 Quick Start (One-liner)

```bash
# Linux/Mac
docker-compose up -d && docker-compose exec web python manage.py migrate

# Windows (PowerShell)
docker-compose up -d; docker-compose exec web python manage.py migrate

# Windows (CMD)
docker-compose up -d && docker-compose exec web python manage.py migrate
```

---

## 📋 Essential Commands

| Task | Command |
|------|---------|
| **Build images** | `docker-compose build` |
| **Start containers** | `docker-compose up -d` |
| **Stop containers** | `docker-compose down` |
| **View logs** | `docker-compose logs -f` |
| **Run migrations** | `docker-compose exec web python manage.py migrate` |
| **Collect static files** | `docker-compose exec web python manage.py collectstatic --noinput` |
| **Create superuser** | `docker-compose exec web python manage.py createsuperuser` |
| **Database shell** | `docker-compose exec db psql -U atm_user -d atm_db` |
| **Django shell** | `docker-compose exec web python manage.py shell` |

---

## 🔗 Access Points

- **Web UI**: http://localhost (Nginx with static files)
- **Direct Django**: http://localhost:8000
- **Admin Panel**: http://localhost/admin/
- **PostgreSQL**: localhost:5432/atm_db

---

## 🔐 Default Credentials

**Database:**
- User: `atm_user`
- Password: `atm_password`
- Database: `atm_db`
- Host: `db` (from container) / `localhost` (from host)

**Email (for testing):**
- Host: `smtp-relay.brevo.com`
- Update `.env` with your credentials

---

## 🛠️ Using Makefile

If you have `make` installed:

```bash
make help       # Show all commands
make build      # Build images
make up         # Start containers
make down       # Stop containers
make migrate    # Run migrations
make static     # Collect static files
make logs       # View logs
make clean      # Clean everything
```

---

## 💻 Using Helper Scripts

### Windows Batch (CMD)
```cmd
docker-cli.bat build
docker-cli.bat up
docker-cli.bat migrate
```

### Windows PowerShell
```powershell
.\docker-cli.ps1 build
.\docker-cli.ps1 up
.\docker-cli.ps1 migrate
```

---

## 📁 File Structure

```
DKG_ATM/
├── Dockerfile           # Docker image definition
├── docker-compose.yml   # Multi-container setup
├── nginx.conf          # Nginx reverse proxy config
├── .env.docker         # Environment variables template
├── DOCKER_GUIDE.md     # Full Docker documentation
├── docker-cli.bat      # Windows batch helper
├── docker-cli.ps1      # Windows PowerShell helper
├── Makefile            # Unix Makefile commands
└── static/             # Static files (CSS, JS, etc)
    ├── BankInterface/
    │   ├── css/
    │   └── js/
    └── UserInterface/
        ├── css/
        └── js/
```

---

## 🔧 Troubleshooting

### Port 8000 is in use
```bash
# Find and kill process
lsof -i :8000
kill -9 <PID>
```

### Database connection fails
```bash
# Check database logs
docker-compose logs db

# Test connection
docker-compose exec web python manage.py dbshell
```

### Static files not loading
```bash
# Recollect static files
docker-compose exec web python manage.py collectstatic --noinput --clear

# Restart Nginx
docker-compose restart nginx
```

### Permission denied errors
```bash
# Fix permissions
docker-compose exec web chown -R appuser:appuser /app
```

---

## 📊 Monitoring

```bash
# View running containers
docker-compose ps

# View all logs in real-time
docker-compose logs -f

# View specific service logs
docker-compose logs -f web
docker-compose logs -f db

# Check resource usage
docker stats
```

---

## 🚀 Production Deployment

Before deploying to production:

1. **Update `.env`:**
   ```
   DEBUG=False
   SECRET_KEY=<generate-strong-key>
   ALLOWED_HOSTS=yourdomain.com
   ```

2. **Set up SSL/TLS** in `nginx.conf`

3. **Change database credentials**

4. **Configure email settings**

5. **Set up backups** for PostgreSQL

6. **Enable log rotation**

---

## 📚 Documentation

- **Full Guide**: See [DOCKER_GUIDE.md](DOCKER_GUIDE.md)
- **Docker Docs**: https://docs.docker.com/
- **Django Deployment**: https://docs.djangoproject.com/en/5.0/howto/deployment/

---

## 💡 Tips

- Use `docker-compose build --no-cache` to rebuild from scratch
- Use `docker-compose up` (without `-d`) to see all logs in terminal
- Use `docker volume ls` to see all volumes
- Use `docker ps -a` to see all containers (including stopped)
- Add `healthcheck` in docker-compose.yml for production

---

## 📞 Common Issues

| Issue | Solution |
|-------|----------|
| "Container already in use" | Run `docker-compose down -v` |
| "Cannot connect to database" | Check `docker-compose logs db` |
| "Static files 404" | Run `docker-compose exec web python manage.py collectstatic --noinput` |
| "Permission denied" | Run with `sudo` or add user to docker group |
| "Out of disk space" | Run `docker system prune -a` |

---

Last Updated: 2024
