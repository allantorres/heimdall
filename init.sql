-- Cria a extensão TimescaleDB no banco de dados padrão
CREATE EXTENSION IF NOT EXISTS timescaledb;

-- Cria um banco de dados de exemplo para seu projeto
CREATE DATABASE heimdall;

-- Cria um usuário para seu projeto (substitua 'myuser' e 'mypassword' por suas credenciais)
CREATE USER allantorres WITH ENCRYPTED PASSWORD 'password1234';
GRANT ALL PRIVILEGES ON DATABASE heimdall TO allantorres;