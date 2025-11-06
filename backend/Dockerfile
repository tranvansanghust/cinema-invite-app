FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
# Copy SQL schema for MySQL initialization
COPY scripts/create_tables.sql /app/scripts/create_tables.sql

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]