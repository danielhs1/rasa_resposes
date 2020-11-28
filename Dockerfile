FROM python:3.8-slim-buster

WORKDIR /srv

# UPDATE APK CACHE AND INSTALL PACKAGES
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    jq \
    tzdata \
    gcc \
    g++ \
    ca-certificates \
    wget && \
    update-ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# INSTALL AWS DEPS
RUN cp /usr/share/zoneinfo/America/Sao_Paulo /etc/localtime && \
    echo "America/Sao_Paulo" > /etc/timezone

# ADD Pipefile.lock
ADD Pipfile* ./

# INSTALL FROM Pipefile.lock FILE
RUN pip install --no-cache -U pip pipenv && pipenv install --system

RUN apt-get remove --purge -y \
    tzdata \
    gcc \
    g++ \
    wget && rm -rf /var/lib/apt/lists/* \
    && apt-get autoremove -y

# ADD APP
ADD . .

EXPOSE 80

# RUN BUILD
RUN chmod +x /srv/app.sh

# ENTRYPOINT
ENTRYPOINT ["/srv/app.sh"]