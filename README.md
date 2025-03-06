# HORIZON.

Horizon is the go-to hub for Commune AI—bringing the buzz together, to the community, from the community, and by the community.communex

* Measures a miner’s influence based on followers, tweets, and other activity.
* Evaluates a tweet’s performance by comparing its engagement metrics .
* Checks how relevant a miner’s tweets are to the subnet’s focus.

## Miner

#### Clone Repository

[https://github.com/loshanparajuli/twitter-GLOBAL]

```shell
git clone https://github.com/loshanparajuli/twitter-GLOBAL
```

#### Env configuration

https://github.com/horizon/-subnet/tree/main#env-configuration

Navigate to miner directory and copy the `.env.miner.example` file to `.env.miner.mainnet`.

```shell
cd miner
cp env/.env.miner.example .env.miner.mainnet
cp .env.example .env
```

Create miner dashboard password hash:

```shell
cd src
pip install passlib
python3 src/subnet/miner_dashboard/generate_pwd_hash.py {your password}
```

Now edit the `.env.miner.mainnet` file to set the appropriate configurations:

```shell
NET_UID=22
MINER_KEY=miner
MINER_NAME=embrace::{miner name}
PORT=9951
POSTGRES_USER=postgres
POSTGRES_PASSWORD=changeit456$
POSTGRES_HOST=localhost
POSTGRES_PORT=5410
POSTGRES_DB=miner
DATABASE_URL=postgresql+asyncpg://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DB}
USER_ID= #your twitter account user id, account must have verified status get your id from https://tweethunter.io/twitter-id-converter
DASHBOARD_USER_NAME=#your miner dashboard login
DASHBOARD_USER_PASSWORD_HASH=#your miner dashboard password hash
```

Ensure that the `.env` file is properly configured:

```shell
DATABASE_URL_MINER=postgresql+asyncpg://postgres:changeit456$@localhost:5410/miner
DATABASE_URL_VALIDATOR=postgresql+asyncpg://postgres:changeit456$@localhost:5420/validator
```

#### Miner wallet creation

[](https://github.com/loshanparajuli/twitter-GLOBAL/embrace-subnet/tree/main#miner-wallet-creation)

```shell
comx key create miner1
comx key list
# transfer COMAI to your miner wallet for registration (aprox 10 COMAI are needed)
comx module register miner embrace::{miner name} 22 --port 9951
```

### Running the miner and monitoring

/embrace-subnet/tree/main#running-the-miner-and-monitoring)

Navigate to `ops` directory, create `.env` file and copy the content from `.env.example` file. Then run the following commands:

```shell
docker compose up -d
```

This will start postgres database

```shell
# use pm2 to run the miner
pm2 start ./scripts/run_miner.sh --name miner
pm2 start ./scripts/run_miner_dashboard.sh --name miner-dashboard
pm2 save
```

## Validator

#### Clone Repository

[(https://github.com/loshanparajuli/twitter-GLOBAL/tree/main/src/subnet)]

```shell
[(https://github.com/loshanparajuli/twitter-GLOBAL/tree/main/src/subnet/validator)]
```

#### Env configuration

[(https://github.com/horizon/horizon-subnet/tree/main#env-configuration-1)]

Navigate to validator directory and copy the `.env.validator.example` file to `.env.validator.mainnet`.

```shell
cd ~/validator
cp ./env/.env.validator.example ./env/.env.validator.mainnet
cp .env.example .env
```

Now edit the `.env.validator.mainnet` file to set the appropriate configurations.

```shell
NET_UID=22
VALIDATOR_KEY=<your_validator_comx_key>
POSTGRES_DB=validator
POSTGRES_USER=postgres
POSTGRES_PASSWORD=changeit456$
DATABASE_URL=postgresql+asyncpg://postgres:changeit456$@localhost:5420/validator

API_RATE_LIMIT=1000
REDIS_URL=redis://localhost:6370/0
LLM_API_KEY={put_proper_value_here}
LLM_TYPE=openai
PORT=9900
WORKERS=1
TWITTER_BEARER_TOKENS= #you have to create twitter (X) developer account, create new project, create new app, and get bearer token to put here
```

Ensure that the `.env` file is properly configured:

```shell
DATABASE_URL_MINER=postgresql+asyncpg://postgres:changeit456$@localhost:5410/miner
DATABASE_URL_VALIDATOR=postgresql+asyncpg://postgres:changeit456$@localhost:5420/validator
```

#### Validator wallet creation

[](https://github.com/horizon/horizon-subnet/tree/main#validator-wallet-creation)

```shell
comx key create validator
comx key list
# transfer COMAI to your validator wallet for registration (aprox 10 COMAI are needed)
comx module register validator validator 20 --port 9900
# stake COMAI to your validator wallet
```

### Running the validator and monitoring

[](https://github.com/horizon/horizon-subnet/tree/main#running-the-validator-and-monitoring)

Start required infrastructure by navigating to ops directory and running the following commands:

```shell
cd ./ops/validator
docker compose up -d
```

Then run the validator:

```shell
# use pm2 to run the validator
cd ~/validator
pm2 start ./scripts/run_validator.sh --name validator
pm2 save
```

Or run the validator in auto update mode:

```shell
cd ~/validator
pm2 start ./scripts/run_validator_auto_update.sh --name validator -- mainnet validator
pm2 save
```

### Running the validator dashboard

[](https://github.com/horizon/horizon-subnet/tree/main#running-the-validator-dashboard)

```shell
cd ~/validator
pm2 start ./scripts/run_validator_dashboard.sh --name validator-dashboard
pm2 save
```

Or run the miner leaderboard in auto update mode:

```shell
cd ~/validator
pm2 start ./scripts/run_validator_dashboard_auto_update.sh --name validator-dashboard -- mainnet validator-dashboard
pm2 save
```

