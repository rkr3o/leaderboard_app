# leaderboard_app

## Running with New Relic Monitoring (Docker)

### 1. Build the New Relic base image
```sh
docker build -f Dockerfile.newrelic -t python_newrelic:latest .
```

### 2. Build your Django app image
```sh
docker build -t my_python_api .
```

### 3. Run your app container with New Relic environment variables
```sh
docker run \
-e NEW_RELIC_LICENSE_KEY=YOUR_LICENSE_KEY \
-e NEW_RELIC_APP_NAME="GlobetrotterGamingBackend" \
-p 8000:8000 -it --rm --name my_python_api_container my_python_api:latest
```

- Replace `YOUR_LICENSE_KEY` with your actual New Relic license key.
- The app will be available at http://localhost:8000
- Check your New Relic dashboard for monitoring data.
