FROM python:3.12-alpine

WORKDIR /app

# Copy relevant project files
COPY src/main ./main
COPY src/cli_main.py .
# Example SBOM copied until files can be sent in from host
COPY example-SBOM.json .

# Create, activate, and setup python virtual environment
RUN python3 -m venv /app/venv
ENV PATH="/app/venv/bin:$PATH"
RUN python -m pip install -r main/requirements.txt

# Copy scorecard binary and make it executable
COPY src/main/scorecard-build/scorecard /usr/local/bin/scorecard
RUN chmod +x /usr/local/bin/scorecard

# Pass the GitHub authentication token from the host environment to the Docker environment
ENV GITHUB_AUTH_TOKEN=$GITHUB_AUTH_TOKEN

# Prevent Python from writing .pyc files to disk (useful in development)
ENV PYTHONDONTWRITEBYTECODE=1
# Prevent Python from buffering stdout and stderr (useful in development)
ENV PYTHONUNBUFFERED=1

# Creates a non-root user with an explicit UID and adds permission to access the app/ folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

ENTRYPOINT [ "python", "cli_main.py" ]
