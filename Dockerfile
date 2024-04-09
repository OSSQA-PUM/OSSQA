# Use an official Python runtime as a parent image
FROM python:3.12-alpine

# Set the working directory in the container to /app
WORKDIR /app

# Copy the requirements file into the Docker image
COPY requirements.txt .

# Copy the contents of the local src directory into the app directory in the Docker image
COPY /src /app

# Copy the scorecard binary into the /usr/local/bin directory in the Docker image
COPY src/scorecard-build/scorecard /usr/local/bin/scorecard

# Make the scorecard binary executable
RUN chmod +x /usr/local/bin/scorecard

# Create a virtual environment in the /app/venv directory
RUN python -m venv /app/venv

# Add the virtual environment binaries to the PATH for subsequent commands
ENV PATH="app/venv/bin:$PATH"

# Install the Python packages listed in requirements.txt
RUN python -m pip install -r requirements.txt

# Prevent Python from writing .pyc files to disk (useful in development)
ENV PYTHONDONTWRITEBYTECODE=1

# Prevent Python from buffering stdout and stderr (useful in development)
ENV PYTHONUNBUFFERED=1

# Pass the GitHub authentication token from the host environment to the Docker environment
ENV GITHUB_AUTH_TOKEN=$GITHUB_AUTH_TOKEN

# Creates a non-root user with an explicit UID and adds permission to access the app/ folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser .
USER appuser

# Run src/__main__.py when the container is launched

#ENTRYPOINT ["python", "__main__.py", "&"]
