COINBASE-TO-TRANSACTIONS
========================

# DEV

## PYTHON

```
if [ ! -d ".venv" ]
then
    pyenv install 3.9.5
    pyenv local 3.9.5 
    pip install virtualenv
    virtualenv .venv
fi
```

## DB

```shell
    $ mkdir -p postgres-data
    $ docker run -it --rm --name some-postgres -v `pwd`/postgres-data:/var/lib/postgresql/data -p 5432:5432 -e POSTGRES_PASSWORD=dbpsql -e POSTGRES_USER=dbpsql -e POSTGRES_DB=dbpsql postgres:11.5
```

### Init DB

run it if something in the schema is changed

```bash
    $ cd postgresql-liquibase
    $ docker run -it -v `pwd`:/drivers -v `pwd`/liquibase.yml:/liquibase.yml --link some-postgres:postgres -e "LIQUIBASE_URL=jdbc:postgresql://postgres/dbpsql" -e "LIQUIBASE_USERNAME=dbpsql" -e "LIQUIBASE_PASSWORD=dbpsql" skillbillsrl/liquibase update
```

## BATCH

```
. .venv/bin/activate
cd application/batch
pip install -r requirements.txt
cd ..
LOG_LEVEL=DEBUG ENV=DEV python batch_server.py
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

## CONNECT DB

```shell

cd /var/lib/buddy
docker exec -it buddy_postgresql_1 psql -U dbpsql

```
