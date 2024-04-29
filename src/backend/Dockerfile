FROM python:3.12-alpine

WORKDIR /app

# Setup virtual environment
RUN python3 -m venv venv

# Activate virtual environment for subsequent commands
ENV PATH="/app/venv/bin:$PATH"

# Copy the application source and requirements
COPY ./src/backend ./backend
COPY ./src/backend_main.py /app/backend_main.py
COPY ./src/backend/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

ENV GITHUB_AUTH_TOKEN=$GITHUB_AUTH_TOKEN
CMD [ "python", "backend_main.py"]
