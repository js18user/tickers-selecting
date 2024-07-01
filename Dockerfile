# syntax=docker/dockerfile:1

FROM python:3.10.9-slim-buster

LABEL maintainer="Jurij <js18.user@gmail.com>"

ENV PYTHONDONTWRITEBYTECODE=1

ENV PYTHONUNBUFFERED=1

COPY requirements.txt .

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

COPY m8_sql_query.py .

COPY m8query.yaml .

COPY m8binance.py .

COPY m8poloniex.py .

COPY main.py .

CMD ["main.py" ]

ENTRYPOINT ["python"]