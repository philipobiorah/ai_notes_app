
# Dockerfile
FROM python:3.10

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN python -m textblob.download_corpora


COPY ./app ./app

RUN mkdir -p /app/app/data
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
