PERSONAL-FINANCE
================

[![buddy pipeline](https://app.buddy.works/skillbill-bw/personal-finance/pipelines/pipeline/373011/badge.svg?token=107d3bbbb60ecabcdb08e0c4f842888977cc5d7b269e84936f8b8074747daf78 "buddy pipeline")](https://app.buddy.works/skillbill-bw/personal-finance/pipelines/pipeline/373011)

[DEMO](https://personal-finance.toto-castaldi.com/) (demo@demo.com / demo1234)

![Demo Portfolio](Screenshot_2022-03-19_10-57-23.png)

# INTEGRATIONS

## GENERAL

* [Coinapi](https://www.coinapi.io/) for Crypto rates

## USER

* [Coinbase](https://www.coinbase.com/) USER Coinbase exchange transactions
* [Blockchain.com](https://www.blockchain.com/api) USER Bitcoin amount
* [Etherscan](https://etherscan.io/apis) USER Ethereum and RC20 Tokens amount
* [Fintable](https://fintable.io/) USER Bank account balance


# DEV

## PYTHON

```
if [ ! -d ".venv" ]
then
    pyenv install 3.10.2
    pyenv local 3.10.2
    pip install virtualenv
    virtualenv .venv
fi
```

## DB

```shell
mkdir -p postgres-data
docker run -it --rm --name some-postgres -v `pwd`/postgres-data:/var/lib/postgresql/data -p 5432:5432 -e POSTGRES_PASSWORD=dbpsql -e POSTGRES_USER=dbpsql -e POSTGRES_DB=dbpsql postgres:11.5
```

### Init DB

run it if something in the schema is changed

```shell
cd postgresql-liquibase
docker run -it -v `pwd`:/drivers -v `pwd`/liquibase.yml:/liquibase.yml --link some-postgres:postgres -e "LIQUIBASE_URL=jdbc:postgresql://postgres/dbpsql" -e "LIQUIBASE_USERNAME=dbpsql" -e "LIQUIBASE_PASSWORD=dbpsql" skillbillsrl/liquibase update
```

## BATCH

```shell
. .venv/bin/activate
cd application/batch
pip install -r requirements.txt
cd ..
LOG_LEVEL=DEBUG ENV=DEV ETHERSCAN_KEY=[KEY] COINAPI_KEY=[KEY] DEMO_ACCOUNT_ID=[ACCOUNT_ID] python batch_server.py
```

## API

```shell
. .venv/bin/activate
cd application/api
pip install -r requirements.txt
cd ..
LOG_LEVEL=DEBUG ENV=DEV python api_server.py
```

## FE

```shell
cd site
npm install
npm run dev
```

# CLOUD SERVER

## INSTALLATION

The server is a Linux Ubuntu 20.04 (LTS) x64

```shell
apt-get update
apt upgrade
apt-get install \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg \
    lsb-release
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
echo \
  "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
apt-get update
apt-get install docker-ce docker-ce-cli containerd.io
apt install curl
curl -L "https://github.com/docker/compose/releases/download/1.26.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose
```

```shell
apt-get update
apt-get install nginx
apt install certbot python3-certbot-nginx
rm /etc/nginx/sites-enabled/*
vi /etc/nginx/sites-enabled/default
# VER 1
systemctl reload nginx
certbot --nginx -d personal-finance.toto-castaldi.com
systemctl reload nginx
vi /etc/nginx/sites-enabled/default
# VER 2
systemctl reload nginx
```

### VER1

```
server {
    listen 80 default_server;
    listen [::]:80 default_server;
    root /var/www/html;
    server_name personal-finance.toto-castaldi.com;
}
```

### VER2

add this

```
location / {
    proxy_pass http://127.0.0.1:8080;
    add_header Cache-Control 'must-revalidate, proxy-revalidate, max-age=0';
}

location /api {
    rewrite ^/api/(.*)$ /$1 break;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_pass http://127.0.0.1:5000;
}
```

## LOCAL BUILD

# MOBILE

```bash
docker run -it -v `pwd`:/app skillbillsrl/android-builder /app/build-app.sh
```


## CONNECT DB

```shell

cd /var/lib/buddy
docker exec -it buddy_postgresql_1 psql -U dbpsql

```
