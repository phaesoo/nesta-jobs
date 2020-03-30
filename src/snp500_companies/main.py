import os
import numpy as np
import yaml
from argparse import ArgumentParser
from urllib.request import urlopen
from bs4 import BeautifulSoup

from sdk.db.mysql import MySQLClient


def parse_options():
    parser = ArgumentParser()
    parser.add_argument("--config_path", dest="config_path", type=str, required=True)
    return parser.parse_args()


def main(configs):
    assert isinstance(configs, dict)

    html = urlopen("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies")
    parsed = BeautifulSoup(html, "html.parser")

    table_rows = parsed.body.find("table", id="constituents").find_all("tr")

    print (f"Total rows: {len(table_rows)}")

    table_headers = table_rows[0].find_all("th")
    table_headers = [s.text.rstrip("\n").strip().lower() for s in table_headers]

    # get target column index list
    column_names = ["symbol", "security", "gics sector", "gics sub industry", "cik"]

    ci_list = list()
    for target in column_names:
        if target not in table_headers:
            raise ValueError(f"Table header might be changed: {target}, {table_headers}")
        ci_list.append(table_headers.index(target))

    data_list = list()
    for tr in table_rows[1:]:
        td_list = np.array(tr.find_all("td"))
        data_list.append([s.text.rstrip("\n").strip() for s in td_list[ci_list]])

    print (f"Insert data to db: {len(table_rows)}")
    sql = """
    INSERT INTO snp500_companies(pit_date, symbol, security, gics_sector, gics_sub_industry, cik)
    VALUES (now(), %s, %s, %s, %s, %s)
    """

    client = MySQLClient()
    client.init(**configs["mysql"])
    try:
        client.executemany(sql=sql, parameter=data_list)
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
    