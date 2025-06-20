FROM python:3.11

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN python -m playwright install-deps
RUN python -m playwright install
RUN apt update && \
    apt install -y \
    libnss3 \
    libnspr4 \
    libdbus-1-3 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libxkbcommon0 \
    libatspi2.0-0 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxrandr2 \
    libgbm1 \
    libasound2 \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

COPY . .

CMD bash -c '\
  for i in {1..30}; do \
    nc -z db 3306 && break; \
    echo "⏳ Waiting for MySQL..."; \
    sleep 2; \
  done; \
  python -m scripts.init_db && python main.py'
