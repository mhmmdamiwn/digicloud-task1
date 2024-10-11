FROM python:3.9-slim

RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    libffi-dev \
    gcc \
    python3-dev
    
WORKDIR /usr/src/app

COPY . .

ENV PYTHONPATH=/usr/src/app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["nameko", "run", "--config", "config.yml", "service"]