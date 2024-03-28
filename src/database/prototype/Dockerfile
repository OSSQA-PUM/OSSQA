FROM python:3.11-alpine

WORKDIR /app

# Setup virtual environment
RUN python3 -m venv /app/venv

# Activate virtual environment for subsequent commands
ENV PATH="/app/venv/bin:$PATH"

# Copy the application source and requirements
COPY ./src/database/prototype /app
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY src/scorecard-build/scorecard /usr/local/bin/scorecard
RUN chmod +x /usr/local/bin/scorecard

# Environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

ENV GITHUB_AUTH_TOKEN=$GITHUB_AUTH_TOKEN

CMD [ "python", "prototype.py" ]