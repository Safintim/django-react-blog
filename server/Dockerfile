FROM python:3.10.0-slim-buster

ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update -qq \
    && DEBIAN_FRONTEND=noninteractive apt-get install -yq --no-install-recommends \
        apt-transport-https \
        build-essential \
        ca-certificates \
        curl \
        git \
        gnupg \
        jq \
        less \
        libpcre3 \
        libpcre3-dev \
        openssh-client \
        telnet \
        unzip \
        vim \
        wait-for-it \
        wget \
    && apt-get clean \
    && rm -rf /var/cache/apt/archives/* \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* \
    && truncate -s 0 /var/log/*log

RUN  \
  echo "deb http://apt.postgresql.org/pub/repos/apt/ buster-pgdg main" > /etc/apt/sources.list.d/nodesource.list \
  && wget -qO- https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add -

RUN apt-get update -qq \
    &&  DEBIAN_FRONTEND=noninteractive apt-get install -yq --no-install-recommends \
         nodejs \
         postgresql-client-12 \
    && apt-get clean \
    && rm -rf /var/cache/apt/archives/* \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* \
    && truncate -s 0 /var/log/*log

RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | python -

ENV PATH="${PATH}:/root/.local/bin"

RUN poetry config virtualenvs.create false

RUN mkdir -p /app
WORKDIR /app

COPY pyproject.toml poetry.lock ./
RUN poetry install  --no-interaction --no-ansi

ADD . /app
ENV DJANGO_SETTINGS_MODULE="blog.settings"

EXPOSE 8000

CMD uwsgi --http :8000 --module blog.wsgi --enable-threads
