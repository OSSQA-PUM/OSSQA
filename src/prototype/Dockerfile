FROM golang:alpine as builder

# Install build dependencies
RUN apk add --no-cache git

# Clone the source code of Security Scorecards
WORKDIR /src
COPY ./src/scorecard scorecard

#RUN git clone https://github.com/ossf/scorecard.git && \
#    cd scorecard

# Build the binary
WORKDIR /src/scorecard
RUN CGO_ENABLED=0 go build -o /scorecard .

FROM alpine

WORKDIR /app

# Install Python and pip
RUN apk add --update --no-cache python3 py3-pip && \
    ln -sf python3 /usr/bin/python

# Setup virtual environment
RUN python3 -m venv /app/venv

# Activate virtual environment for subsequent commands
ENV PATH="/app/venv/bin:$PATH"

# Copy the application source and requirements
COPY ./src/prototype /app
COPY requirements.txt .

# Install Python dependencies in the virtual environment
RUN pip install --no-cache-dir -r requirements.txt

# Copy the scorecard binary from the builder stage
COPY --from=builder /scorecard /usr/local/bin/scorecard

# Ensure the binary is executable
RUN chmod +x /usr/local/bin/scorecard

# Environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

#ENV GITHUB_AUTH_TOKEN=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
ENV GITHUB_AUTH_TOKEN=$GITHUB_AUTH_TOKEN

#CMD ["scorecard", "--repo=https://github.com/OSSQA-PUM/OSSQA", "--show-details"- "--format json"]
CMD [ "python", "prototype.py" ]