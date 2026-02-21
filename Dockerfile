FROM ghcr.io/astral-sh/uv:0.9.7 AS uv-stage
FROM python:3.14-slim

# Install dependencies
RUN apt-get update && apt-get install -y \
    wget \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libgbm1 \
    libgtk-3-0 \
    libnspr4 \
    libnss3 \
    ca-certificates \
    curl \
    jq \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# Download and install Google Chrome (stable) for amd64
RUN wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    apt-get update && apt-get install -y ./google-chrome-stable_current_amd64.deb && \
    rm google-chrome-stable_current_amd64.deb && \
    rm -rf /var/lib/apt/lists/*

# Download and install matching chromedriver version
RUN CHROME_VERSION=$(google-chrome --version | awk '{print $3}') && \
    echo "Installed Chrome version: $CHROME_VERSION" && \
    wget "https://storage.googleapis.com/chrome-for-testing-public/${CHROME_VERSION}/linux64/chromedriver-linux64.zip" && \
    unzip chromedriver-linux64.zip && \
    mv chromedriver-linux64/chromedriver /usr/bin/chromedriver && \
    chmod +x /usr/bin/chromedriver && \
    rm -rf chromedriver-linux64 chromedriver-linux64.zip

WORKDIR /selenium-wrapper

# Install uv
COPY --from=uv-stage /uv /uvx /bin/

# Copy files needed for uv
COPY pyproject.toml uv.lock ./

# Install dependencies using uv
RUN uv sync --frozen --no-install-project

# Copy the rest of the application code
COPY . .

ENV PATH="/selenium-wrapper/.venv/bin:$PATH"

# Set display port to avoid crash
ENV DISPLAY=:99

# Run tests using pytest
CMD ["sh", "-c", "pytest tests/ -v -m ${MARKER:-'not slow'} -n ${NUM_CORES:-2}"]
