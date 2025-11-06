# Docker Commands Guide

## Important: Use `docker compose` (not `docker-compose`)

Docker Compose V2 is integrated into Docker CLI. Use the command **without the hyphen**.

## Common Commands

### Start Services
```bash
docker compose up -d
```

### Stop Services
```bash
docker compose down
```

### View Logs
```bash
docker compose logs -f
```

### View Running Services
```bash
docker compose ps
```

### Rebuild and Start
```bash
docker compose up -d --build
```

### Stop and Remove Volumes
```bash
docker compose down -v
```

## Troubleshooting

If you get the error: `"Not supported URL scheme http+docker"`

**Solution:** Use `docker compose` (without hyphen) instead of `docker-compose`

The old `docker-compose` command from Anaconda or standalone installation is incompatible with newer Docker versions.

