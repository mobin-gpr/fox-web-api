FROM python:3.12.3-alpine

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PATH="/PY/BIN:$PATH"

RUN pip install --upgrade pip

COPY . /app

RUN pip install -r requirements.txt