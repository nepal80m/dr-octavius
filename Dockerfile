# syntax=docker/dockerfile:1
FROM python:3.10


ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN mkdir -p /octavius/{src,static,media}
RUN mkdir -p /var/log/octavius

WORKDIR /octavius/src/

COPY ./requirements.txt /octavius/src/requirements.txt

RUN pip install -r requirements.txt

COPY . /octavius/src/
RUN chmod +x ./docker_init.sh
EXPOSE 8000
CMD ["./docker_init.sh" ]
