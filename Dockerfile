FROM ubuntu:22.04

ENV TZ=UTC
ENV DEBIAN_FRONTEND=noninteractive

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        python3-dev \
        build-essential \
        libpq-dev \ 
        && rm -rf /var/lib/apt/lists/*

WORKDIR /root/project/backend

COPY backend /root/project/backend

RUN pip3 install --no-cache-dir -r /root/project/backend/requirements.txt
RUN pip install gunicorn
RUN pip install psycopg2-binary

EXPOSE 8000

CMD gunicorn backend.wsgi:application --bind 0.0.0.0:$PORT
