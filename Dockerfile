FROM python:3.7-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code

COPY requirements.txt .
RUN pip install -r requirements.txt
#COPY ./entrypoint.sh ./entrypoint.sh
#ENTRYPOINT ["./entrypoint.sh"]

COPY . /code/
EXPOSE 8000