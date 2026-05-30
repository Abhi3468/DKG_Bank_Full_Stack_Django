# Docker quick start script for ATM Bank (PowerShell version)
# Usage: .\docker-cli.ps1 [command]

param(
    [string]$Command = "help"
)

function Show-Help {
    Write-Host "`nATM Bank Docker Commands" -ForegroundColor Cyan
    Write-Host "========================`n"
    Write-Host "Usage: .\docker-cli.ps1 [command]`n"
    Write-Host "Commands:"
    Write-Host "  help       - Show this help message"
    Write-Host "  build      - Build Docker images"
    Write-Host "  up         - Start all containers"
    Write-Host "  down       - Stop and remove containers"
    Write-Host "  logs       - View container logs"
    Write-Host "  shell      - Access Django shell"
    Write-Host "  bash       - Access container bash"
    Write-Host "  db-shell   - Access PostgreSQL shell"
    Write-Host "  migrate    - Run database migrations"
    Write-Host "  static     - Collect static files"
    Write-Host "  superuser  - Create superuser"
    Write-Host "  test       - Run tests"
    Write-Host "  ps         - Show running containers"
    Write-Host "  clean      - Remove containers and volumes"
    Write-Host "`nExamples:"
    Write-Host "  .\docker-cli.ps1 build"
    Write-Host "  .\docker-cli.ps1 up"
    Write-Host "  .\docker-cli.ps1 logs`n"
}

function Invoke-Command {
    param($Cmd)
    Write-Host "Executing: $Cmd" -ForegroundColor Yellow
    Invoke-Expression $Cmd
}

switch ($Command.ToLower()) {
    "help" {
        Show-Help
    }
    "build" {
        Write-Host "Building Docker images..." -ForegroundColor Green
        docker-compose build
    }
    "up" {
        Write-Host "Starting containers..." -ForegroundColor Green
        docker-compose up -d
        Write-Host "`n✓ Containers started!" -ForegroundColor Green
        Write-Host "  Web: http://localhost"
        Write-Host "  Direct: http://localhost:8000"
        Write-Host "  Database: localhost:5432`n"
    }
    "down" {
        Write-Host "Stopping containers..." -ForegroundColor Green
        docker-compose down
        Write-Host "✓ Containers stopped!`n" -ForegroundColor Green
    }
    "logs" {
        docker-compose logs -f
    }
    "shell" {
        docker-compose exec web python manage.py shell
    }
    "bash" {
        docker-compose exec web bash
    }
    "db-shell" {
        docker-compose exec db psql -U atm_user -d atm_db
    }
    "migrate" {
        Write-Host "Running migrations..." -ForegroundColor Green
        docker-compose exec web python manage.py migrate
        Write-Host "✓ Migrations completed!`n" -ForegroundColor Green
    }
    "static" {
        Write-Host "Collecting static files..." -ForegroundColor Green
        docker-compose exec web python manage.py collectstatic --noinput --clear
        Write-Host "✓ Static files collected!`n" -ForegroundColor Green
    }
    "superuser" {
        docker-compose exec web python manage.py createsuperuser
    }
    "test" {
        docker-compose exec web python manage.py test
    }
    "ps" {
        docker-compose ps
    }
    "clean" {
        Write-Host "Removing containers and volumes..." -ForegroundColor Yellow
        docker-compose down -v
        Write-Host "✓ Cleaned up!`n" -ForegroundColor Green
    }
    default {
        Write-Host "Unknown command: $Command" -ForegroundColor Red
        Show-Help
    }
}
