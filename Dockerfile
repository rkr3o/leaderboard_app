FROM python:3.9.14-alpine3.16

# Install system dependencies
RUN apk add --no-cache bzip2-dev \
        coreutils \
        gcc \
        libc-dev \
        libffi-dev \
        libressl-dev \
        linux-headers

# Install New Relic and Python dependencies
RUN pip install --no-cache-dir newrelic

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

# Use New Relic as the entrypoint for your Django app
ENTRYPOINT ["newrelic-admin", "run-program"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
