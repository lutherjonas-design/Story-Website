FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libpq-dev gcc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /backend

COPY ./requirements.txt ./requirements.txt
RUN pip install --upgrade pip && pip install --no-cache-dir -r /backend/requirements.txt

COPY . .

EXPOSE 8000
CMD ["python", "manage.py","runserver","0.0.0.0:8000"]