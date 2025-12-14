# Dockerfile for LangChain_Env smoke test
FROM python:3.13-slim

# Avoid running as root in production, but keep simple for smoke test
WORKDIR /app

# Install system deps and pip without cache
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better cache
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . /app

# Copy entrypoint and ensure it's executable
COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

# Default entrypoint validates env and runs the command
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
CMD ["python3", "smoke_test.py"]
