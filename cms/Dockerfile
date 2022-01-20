FROM python:3.9-slim-buster

RUN apt-get update
RUN apt-get install libpq-dev -y

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . cms
COPY .env .env

ENV PYTHONPATH=/:/cms

CMD ["python", "cms/main.py"]
