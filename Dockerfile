
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libffi-dev libssl-dev python3-dev sqlite3 pkg-config curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /var/www/html/py-agenticai

COPY requirements.txt .

RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --upgrade pip setuptools wheel && \
    pip install -r requirements.txt

COPY . .

RUN mkdir -p ./chroma_db && \
    useradd -m appuser && \
    chown -R appuser:appuser ./chroma_db

USER appuser

EXPOSE 8000

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
