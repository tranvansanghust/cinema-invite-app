#!/bin/bash
set -e

# Wait for MySQL to be ready
echo "Waiting for MySQL to be ready..."
while ! python -c "import pymysql; pymysql.connect(host='${MYSQL_HOST:-localhost}', port=${MYSQL_PORT:-3306}, user='${MYSQL_USER:-cinema_user}', password='${MYSQL_PASSWORD:-123456}')" 2>/dev/null; do
  echo "MySQL is unavailable - sleeping"
  sleep 1
done

echo "MySQL is up - executing migrations"

# Run Alembic migrations
alembic upgrade head

echo "Migrations completed - starting application"

# Start the application
exec uvicorn main:app --host 0.0.0.0 --port 8000
