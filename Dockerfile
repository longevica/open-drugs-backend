FROM python:3.9-slim-buster

RUN apt-get update
RUN apt-get install libpq-dev -y

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY api api
COPY .env .env
COPY VERSION ./

ENV PYTHONPATH=/:/api

CMD ["python", "api/main.py"]
