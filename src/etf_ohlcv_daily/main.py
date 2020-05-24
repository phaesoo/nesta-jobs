import os
import numpy as np
import yaml
from argparse import ArgumentParser
from utils import get_ohlcv

from sdk.db.mysql import MySQLClient


def parse_options():
    parser = ArgumentParser()
    parser.add_argument("--config_path", dest="config_path", type=str, required=True)
    return parser.parse_args()


def main(configs):
    assert isinstance(configs, dict)

    client = MySQLClient()
    client.init(**configs["mysql"])

    tickers = ["SPY", "VOO", "QQQ", "VXX"]
    
    columns = ["ticker", "date", "open", "high", "low", "close", "volume", "adj_close", "return"]

    query = f"""
    INSERT IGNORE INTO ohlcv_daily({", ".join([f"`{c}`" for c in columns])})
    values(%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    for ticker in tickers:
        try:
            df = get_ohlcv(ticker)
        except Exception as e:
            print ("pandas datareader error", ticker, str(e))
            continue
            
        df["date"] = df.index.map(lambda x: int(x.strftime('%Y%m%d')))
        df["ticker"] = ticker
        
        df = df.reindex(columns=columns)
        df = df.fillna(0.0)

        values = df.values.tolist()

        try:
            client.executemany(sql=query, parameter=df.values.tolist())
            client.commit()
        except Exception as e:
            client.rollback()
            print (e)
            raise ValueError


if __name__ == "__main__":
    options = parse_options()

    config_path = options.config_path
    if not os.path.exists(config_path):
        raise FileNotFoundError(config_path)
    # read from yaml
    configs = yaml.load(open(config_path), Loader=yaml.Loader)
    main(configs=configs)
    