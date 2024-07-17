FROM python:3.10.0-slim-bullseye


WORKDIR /app
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Install necessary Linux packages
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libc-dev python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements files
COPY ./api ./api
COPY requirements.txt ./requirements.txt

# Install dependencies
RUN pip install --upgrade --force-reinstall pip  \
    && pip install --no-cache-dir --force-reinstall -r  ./requirements.txt


EXPOSE 8001


CMD ["gunicorn", "api.main:app", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "--graceful-timeout", "60", "--timeout", "120", "--bind", "0.0.0.0:8001"]
