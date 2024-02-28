# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.11-alpine

WORKDIR /app

# Setup virtual environment
RUN python3 -m venv /app/venv

# Activate virtual environment for subsequent commands
ENV PATH="/app/venv/bin:$PATH"

# Copy scorecard binary
COPY src/scorecard-build/scorecard /usr/local/bin/scorecard
RUN chmod +x /usr/local/bin/scorecard

COPY src/tests/test_requirements.txt .
COPY requirements.txt .
COPY src .
RUN python -m pip install -r test_requirements.txt


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
CMD ["pytest", "tests/test_prototype.py"]