@echo off
REM Docker quick start script for ATM Bank
REM Run this file to quickly manage Docker containers

setlocal enabledelayedexpansion

if "%1"=="" (
    call :show_help
    exit /b 0
)

if /i "%1"=="help" (
    call :show_help
) else if /i "%1"=="build" (
    echo Building Docker images...
    docker-compose build
) else if /i "%1"=="up" (
    echo Starting containers...
    docker-compose up -d
    echo.
    echo ✓ Containers started!
    echo Web: http://localhost
    echo Direct: http://localhost:8000
    echo Database: localhost:5432
) else if /i "%1"=="down" (
    echo Stopping containers...
    docker-compose down
    echo ✓ Containers stopped!
) else if /i "%1"=="logs" (
    docker-compose logs -f
) else if /i "%1"=="shell" (
    docker-compose exec web python manage.py shell
) else if /i "%1"=="bash" (
    docker-compose exec web bash
) else if /i "%1"=="migrate" (
    echo Running migrations...
    docker-compose exec web python manage.py migrate
    echo ✓ Migrations completed!
) else if /i "%1"=="static" (
    echo Collecting static files...
    docker-compose exec web python manage.py collectstatic --noinput --clear
    echo ✓ Static files collected!
) else if /i "%1"=="superuser" (
    docker-compose exec web python manage.py createsuperuser
) else if /i "%1"=="test" (
    docker-compose exec web python manage.py test
) else if /i "%1"=="ps" (
    docker-compose ps
) else (
    echo Unknown command: %1
    call :show_help
    exit /b 1
)
exit /b 0

:show_help
echo.
echo ATM Bank Docker Commands
echo ========================
echo.
echo Usage: docker-cli.bat [command]
echo.
echo Commands:
echo   help       - Show this help message
echo   build      - Build Docker images
echo   up         - Start all containers
echo   down       - Stop and remove containers
echo   logs       - View container logs
echo   shell      - Access Django shell
echo   bash       - Access container bash
echo   migrate    - Run database migrations
echo   static     - Collect static files
echo   superuser  - Create superuser
echo   test       - Run tests
echo   ps         - Show running containers
echo.
echo Examples:
echo   docker-cli.bat build
echo   docker-cli.bat up
echo   docker-cli.bat logs
echo.
