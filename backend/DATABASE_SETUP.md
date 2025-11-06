# Database Setup Guide

This guide explains how to set up and manage the MySQL database for the Cinema Invite App.

## Prerequisites

- Docker and Docker Compose installed
- Python 3.8+ (if running locally)
- Alembic installed (`pip install alembic` or `poetry install`)

## Quick Start with Docker Compose

1. **Start MySQL database:**
   ```bash
   docker-compose up -d mysql
   ```

2. **Run database migrations:**
   ```bash
   cd backend
   alembic upgrade head
   ```

3. **Start the backend application:**
   ```bash
   docker-compose up backend
   ```

## Manual Setup

### 1. Environment Variables

Create a `.env` file in the `backend/` directory with the following variables:

```env
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=123456
MYSQL_DB=cinema_invite_db
DATABASE_URL=mysql+pymysql://root:123456@localhost:3306/cinema_invite_db?charset=utf8mb4
```

### 2. Create Database

If not using Docker, create the database manually:

```sql
CREATE DATABASE cinema_invite_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 3. Run Migrations

```bash
cd backend
alembic upgrade head
```

## Database Migrations with Alembic

### Create a New Migration

```bash
cd backend
alembic revision --autogenerate -m "description of changes"
```

### Apply Migrations

```bash
alembic upgrade head
```

### Rollback Migration

```bash
alembic downgrade -1
```

### View Migration History

```bash
alembic history
```

### View Current Revision

```bash
alembic current
```

## Database Models

The application uses three main models:

1. **User** - User accounts with authentication
2. **Movie** - Movie information
3. **Invitation** - User-created invitations linking users to movies

All models are defined in `backend/app/models/` and use SQLAlchemy ORM.

## Important Notes

- The database uses MySQL 8.0
- All tables use UTF8MB4 encoding for full Unicode support
- Foreign key constraints are enforced
- The `invitations` table stores arrays (image_urls, cinema_ids) as semicolon-separated strings
- Auto-increment is enabled for all primary keys

## Troubleshooting

### Connection Issues

- Verify MySQL is running: `docker-compose ps`
- Check environment variables match your MySQL configuration
- Ensure the database exists: `mysql -u root -p -e "SHOW DATABASES;"`

### Migration Issues

- Check Alembic version: `alembic --version`
- Verify models are imported in `alembic/env.py`
- Check migration files in `alembic/versions/`

### Reset Database

⚠️ **Warning: This will delete all data!**

```bash
# Drop all tables
alembic downgrade base

# Recreate all tables
alembic upgrade head
```

