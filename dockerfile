# Usa a imagem oficial do PostgreSQL
FROM postgres:16

# Instala o TimescaleDB
RUN apt-get update && apt-get install -y wget gnupg2 \
    && wget --quiet -O - https://packagecloud.io/timescale/timescaledb/gpgkey | apt-key add - \
    && echo "deb https://packagecloud.io/timescale/timescaledb/debian/ $(lsb_release -c -s) main" > /etc/apt/sources.list.d/timescaledb.list \
    && apt-get update \
    && apt-get install -y timescaledb-2-postgresql-16 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copia o script de inicialização para criar a extensão TimescaleDB
COPY init.sql /docker-entrypoint-initdb.d/01-init.sql