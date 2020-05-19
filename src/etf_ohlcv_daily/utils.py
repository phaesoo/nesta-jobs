from datetime import datetime
from pandas import DataFrame
import pandas_datareader as pdr


def get_ohlcv(ticker: str, start: datetime = None, end: datetime = None) -> DataFrame:
    assert isinstance(ticker, str), "Type Error"

    df = pdr.DataReader(ticker, "yahoo")
    df = df.rename(
        columns={"High": "high", "Low": "low", "Open": "open",
                 "Close": "close", "Volume": "volume", "Adj Close": "adj_close"}
    )

    # calc return
    adj_close_s = df.adj_close
    df["return"] = adj_close_s.diff() / adj_close_s.shift(1)

    # trim index
    if start:
        df = df[df.index >= start]
    if end:
        df = df[df.index <= end]
    return df
