#!/bin/sh

echo "Applying migrations..."
alembic upgrade head

echo "Starting application..."
exec uvicorn src.api.main:app --host 0.0.0.0 --port 8000