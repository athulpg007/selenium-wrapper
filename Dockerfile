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
    fonts-liberation \
    libasound2 \
    libx11-xcb1 \
    libxcomposite1 \
    libxcursor1 \
    libxdamage1 \
    libxi6 \
    libxrandr2 \
    libxss1 \
    libxtst6 \
    x11-utils \
    curl \
    jq \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# Download and install latest stable Google Chrome for Testing
RUN apt-get update && \
    CHROME_VERSION=$(wget -qO- "https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions-with-downloads.json" | \
    python -c "import sys, json; v=json.load(sys.stdin); print(v['channels']['Stable']['version'])") && \
    wget "https://storage.googleapis.com/chrome-for-testing-public/${CHROME_VERSION}/linux64/chrome-linux64.zip" && \
    unzip chrome-linux64.zip && \
    mv chrome-linux64 /opt/ && \
    ln -s /opt/chrome-linux64/chrome /usr/bin/google-chrome && \
    rm -rf chrome-linux64 chrome-linux64.zip

# Download and install Chromedriver
RUN CHROME_VERSION=$(google-chrome --version | awk '{print $5}') && \
    echo "Installed Chrome version: $CHROME_VERSION" && \
    CHROMEDRIVER_VERSION=$(wget -qO- "https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions-with-downloads.json" | \
	python -c "import sys, json; v=json.load(sys.stdin); print(v['channels']['Stable']['version'])") && \
	wget "https://storage.googleapis.com/chrome-for-testing-public/${CHROMEDRIVER_VERSION}/linux64/chromedriver-linux64.zip" && \
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
