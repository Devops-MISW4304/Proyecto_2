FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# New Relic env vars 
ENV NEW_RELIC_APP_NAME="blacklist-api"
ENV NEW_RELIC_LOG=stdout
ENV NEW_RELIC_DISTRIBUTED_TRACING_ENABLED=true
ENV NEW_RELIC_LOG_LEVEL=info

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt \
    && pip install newrelic

COPY . .

EXPOSE 5000

# Usamos newrelic-admin para arrancar la app
CMD ["newrelic-admin", "run-program", "gunicorn", "--bind", "0.0.0.0:5000", "run:app"]
