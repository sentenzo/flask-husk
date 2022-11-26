FROM python:3.10-slim-buster

RUN apt update && \
    apt install --no-install-recommends --no-install-suggests --assume-yes \
    # For Psycopg
    gcc \
    python3-dev \
    libpq-dev \
    libmagic1

RUN python -m pip install --upgrade pip

WORKDIR /usr/src/app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["gunicorn", "app:app", "-b", ":10000"]