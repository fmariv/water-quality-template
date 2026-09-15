FROM ghcr.io/astral-sh/uv:0.6.17-python3.12-bookworm-slim

WORKDIR /app

RUN apt-get update -y && \
    apt-get install -y --no-install-recommends \
        g++ \
        libgdal-dev && \
    rm -rf /var/lib/apt/lists/*

ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
ENV C_INCLUDE_PATH=/usr/include/gdal

RUN uv venv

COPY requirements.txt .
RUN uv pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uv", "run", "python3", "main.py", "--host", "0.0.0.0", "--port", "8000"]
