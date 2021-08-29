# dca-binance

Small cli python script to buy cryptocurrencies on Binance.

## Installation

```shell
python3 -p pip install -U pip
python3 -m pip install --user .
```

## Usage

Create `config.ini` file

```ini
# Binance API
[API]
secret: XXX
key: XXX

[BUY1]
# What to buy
symbol: BTCUSDT
# Buy 11 EUR worth of BTC
amount: 11

[BUY2]
# What to buy
symbol: ETHUSDT
# Buy 11 EUR worth of ETH
amount: 11
```

then run

```shell
dca-binance
```

By default, `dca-binance` is using `config.ini` in the current path.
You can specify another config file using `--config-file <path_to_config_file>`.

# Development

```shell
python3 -m venv dca-binance-venv
source dca-binance-venv/bin/activate
pip3 install -e .
```

Using black for formatting and flake8, flake8-isort for linting.

