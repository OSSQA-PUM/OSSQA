# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.12-alpine

WORKDIR /app

# Setup virtual environment
RUN python3 -m venv /app/venv

# Activate virtual environment for subsequent commands
ENV PATH="/app/venv/bin:$PATH"

# Copy scorecard binary
COPY src/main/scorecard-build/scorecard /usr/local/bin/scorecard
RUN chmod +x /usr/local/bin/scorecard

COPY src/main/tests/requirements.txt .
COPY src/main .
COPY pytest.ini .
COPY .coveragerc .
RUN python -m pip install -r requirements.txt


ENV GITHUB_AUTH_TOKEN=$GITHUB_AUTH_TOKEN

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1
# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
ENTRYPOINT [ "sh", "/app/tests/run.sh" ]