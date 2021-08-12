import argparse
import configparser
import logging
import sys
from pathlib import Path

from binance.client import Client
from binance.exceptions import BinanceAPIException

from .logger import setup_logger, setup_logger_filename

__author__ = "Louis Aussedat"
__copyright__ = "Copyright (c) 2021 Louis Aussedat"
__license__ = "GPLv3"

log = setup_logger(__name__, logging.INFO)


def check_section(config, section, hard):
    if not config.has_section(section):
        if hard:
            log.error(f"Missing section {section}")
            exit(1)
        else:
            return False
    else:
        return True


def check_option(config, section, option, hard):
    if not config.has_option(section, option):
        if hard:
            log.error(f"Missing option {option} in section {section}")
            exit(1)
        else:
            log.warning(f"Missing option {option} in section {section}, skipping.")
            return False
    else:
        return True


def check_config(config_file, hard):
    if not Path(config_file).is_file():
        if hard:
            log.error(f"No such file {config_file}")
            exit(1)

    config = configparser.ConfigParser()
    config.read(config_file)

    check_section(config, "API", hard)
    check_option(config, "API", "secret", hard)
    check_option(config, "API", "key", hard)

    return config


def main(argv):
    parser = argparse.ArgumentParser(argv)
    parser.add_argument(
        "--config-file", default="./config.ini", help="config file path"
    )
    parser.add_argument("--log-path", help="log file path")
    parser.add_argument("-d", "--debug", help="debug mode", action="store_true")
    parser.add_argument("-n", "--dryrun", help="dry run mode", action="store_true")
    args = parser.parse_args()

    if args.log_path:
        setup_logger_filename(__name__, args.log_path)

    log.info("starting dca-binance")

    if args.debug:
        log.setLevel(logging.DEBUG)
        log.debug("debug mode")

    log.debug(args)

    config = check_config(args.config_file, True)
    log.info(f"using config file {args.config_file}")

    api_key = config["API"]["key"]
    api_secret = config["API"]["secret"]

    client = Client(api_key, api_secret)

    executed_amount = 0

    for i in range(1, 10):

        buy_section_name = f"BUY{i}"
        if not check_section(config, buy_section_name, False):
            continue

        if not check_option(config, buy_section_name, "symbol", False):
            continue

        if not check_option(config, buy_section_name, "ammount", False):
            continue

        symbol = config[buy_section_name]["symbol"]
        ammount = float(config[buy_section_name]["ammount"])

        log.debug(f"symbol: {symbol}")
        log.debug(f"ammount: {ammount}")

        depth = client.get_order_book(symbol=symbol, limit=10)
        avg_price = float(depth["bids"][0][0])

        quantity = ammount / avg_price
        quantity = f"{quantity:.5f}"
        avg_price = f"{avg_price:.2f}"

        log.info(f"{symbol} quantity to buy: {quantity}")
        log.info(f"{symbol} average price: {avg_price}")

        if not args.dryrun:
            try:
                order = client.order_limit_buy(
                    symbol=symbol, quantity=quantity, price=avg_price
                )
            except BinanceAPIException as e:
                log.error(f"{e.message}, result code: {e.status_code}")
                exit(e.status_code)

            log.debug(order)

        executed_amount += 1

    log.info(
        f"executed {executed_amount} limit orders{' (DRYRUN)' if args.dryrun else ''}."
    )


def exec_command_line(argv):
    if main(argv):
        exit(0)
    else:
        exit(255)


if __name__ == "__main__":
    main(sys.argv)
