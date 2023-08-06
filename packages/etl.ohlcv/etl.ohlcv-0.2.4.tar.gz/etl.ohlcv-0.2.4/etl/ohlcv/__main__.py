#!/usr/bin/env python3

"""ETL OHLCV: Command Line Interface."""

from __future__ import annotations

from pathlib import Path
import asyncio
import datetime as dtlib
import json as jsonlib
import os
import sys

import boto3
import ccxt.async_support as ccxt  # noqa: E402
import fire
import pandas as pd

from etl.ohlcv import logging
from etl.ohlcv.table import ExchangeMetadata
from etl.ohlcv.typing import JSONLike
from etl.ohlcv.util.datetime_util import BTC_START
from etl.ohlcv.util.datetime_util import get_datetime
from etl.ohlcv.util.datetime_util import get_datetime_now
from etl.ohlcv.util.datetime_util import get_item_start
from etl.ohlcv.util.datetime_util import get_milliseconds
from etl.ohlcv.util.datetime_util import get_valid_start_end
from etl.ohlcv.util.string_util import generate_id
from etl.ohlcv.util.string_util import lowerstrip
import etl.ohlcv


BUCKET_NAME = os.environ.get("ETL_OHLCV_BUCKET_NAME", "etl-ohlcv-datasets")


# Create local logger
logger = logging.get_logger(__name__)


class ETLOHLCVCommandLineInterface:

    async def index(self, exchange_name: str):
        """Load each exchange and save it's metadata in Dynamo DB."""
        try:
            exchange_name = lowerstrip(exchange_name)
            exchange = getattr(
                ccxt, lowerstrip(exchange_name)
            )({"enableRateLimit": True})

        except AttributeError:
            logger.warning(f"Exchange not available in CCXT: {exchange_name}")
            return

        # Load markets asynchronously
        await exchange.load_markets()
        await exchange.close()

        # Create counter strings for our main loop
        counts = len(exchange.markets)
        counts = [f"{(i + 1):04}/{counts:04}" for i in range(counts)]

        # List of market IDs to be skipped
        skip_keys = [(exchange_name, m["id"]) for _, m in exchange.markets.items()]
        skips = [item.sort_key for item in ExchangeMetadata.batch_get(skip_keys)]

        # Empty list variables that would be used
        # later for batch reads and writes
        writes = []

        for count, (symbol, market) in zip(counts, exchange.markets.items()):
            mid = market["id"]
            if mid in skips:
                continue

            logger.info(
                f"[{count}] Indexing exchange metadata",
                extra={"exchange": exchange.name, "symbol": symbol}
            )

            timestamp_oldest = get_milliseconds(
                await etl.ohlcv.get_oldest_datetime(exchange, symbol)
            )

            if timestamp_oldest is None:
                logger.info(
                    f"[{count}] Skipping, invalid oldest datetime",
                    extra={"exchange": exchange.name, "symbol": symbol}
                )
                continue

            writes.append(
                ExchangeMetadata(
                    exchange_name,
                    sort_key=mid,
                    symbol=symbol,
                    base=market["base"],
                    quote=market["quote"],
                    timestamp_oldest=timestamp_oldest,
                    timestamp_newest=timestamp_oldest,
                )
            )

        # Write items in batch for faster run times
        with ExchangeMetadata.batch_write() as batch:
            for item in writes:
                batch.save(item)

    async def fetch(
        self,
        exchange_name: str,
        symbol: str,
        *,
        show_progress: bool = False,
    ):
        """Load each exchange and save it's metadata in Dynamo DB."""
        s3 = boto3.client("s3")
        timeframe = "1m"

        try:
            exchange_name = lowerstrip(exchange_name)
            exchange = getattr(ccxt, exchange_name)({"enableRateLimit": True})

        except AttributeError:
            logger.warning(f"Exchange not available in CCXT: {exchange_name}")
            return

        # Load markets asynchronously
        await exchange.load_markets()
        await exchange.close()

        if not exchange.markets.get(symbol, {}).get("active", False):
            logger.warning(f"Symbol is not available: {symbol}")
            return

        logger.info(
            f"Fetching OHLCV",
            extra={
                "exchange": exchange_name,
                "timeframe": timeframe,
                "symbol": symbol,
            }
        )

        # Extract relevant parts of the market
        market = exchange.markets[symbol]
        mid = market["id"]
        base = market["base"]
        quote = market["quote"]

        # Don't proceed with fetching if 1d item does not exist
        item = ExchangeMetadata.fetch(exchange_name, mid)
        if item is None:
            logger.warning(
                "Skipping OHLCV fetch, Dynamo DB item does not exist",
                extra={
                    "partition_key": exchange_name,
                    "sort_key": mid,
                }
            )
            return

        start = get_datetime(item.timestamp_newest)
        end = start + dtlib.timedelta(days=7)
        now = get_datetime_now()

        # Fetch OHLCV. If there is no entry or item yet,
        # use Bitcoin's creation as the oldest date and "now"
        # as the newest only if the respective item is missing
        start, end = get_valid_start_end(
            start, end, timeframe, include_latest=False, now=now
        )

        file = etl.ohlcv.generate_filepath(exchange_name, symbol, timeframe)
        fileuri = etl.ohlcv.generate_s3_fileuri(
            BUCKET_NAME, exchange_name, symbol, timeframe
        )

        try:
            old_ohlcvs = pd.read_parquet(fileuri, engine="pyarrow")
        except FileNotFoundError:
            old_ohlcvs = pd.DataFrame()

        ohlcvs = await etl.ohlcv.fetch(
            exchange_name,
            symbol,
            timeframe,
            start=start,
            end=end,
            now=now,
            show_progress=show_progress,
        )

        # If the OHLCV is empty, don't even bother proceeding
        if ohlcvs.empty:
            logger.warning(
                "Fetched OHLCV is empty",
                extra={
                    "exchange_name": exchange_name,
                    "timeframe": timeframe,
                    "symbol": symbol,
                    "start": start,
                    "end": end,
                    "now": now,
                }
            )
            return

        ohlcvs = pd.concat([old_ohlcvs, ohlcvs])
        ohlcvs = etl.ohlcv.unique(ohlcvs)

        # Upload the file using boto3 to enable parallel upload
        try:
            ohlcvs.to_parquet(file, engine="pyarrow")
        except (FileNotFoundError, OSError):
            Path(file.parent).mkdir(parents=True, exist_ok=True)
            ohlcvs.to_parquet(file, engine="pyarrow")

        with open(file, "rb") as fp:
            s3.upload_fileobj(fp, BUCKET_NAME, str(file).replace("\\", "/"))

        timestamp_newest = get_milliseconds(ohlcvs.index[-1])
        logger.info(
            "Updating latest timestamp",
            extra={"timestamp_newest": timestamp_newest}
        )

        ExchangeMetadata(
            hash_key=exchange_name,
            range_key=mid,
        ).update(
            actions=[
                ExchangeMetadata.timestamp_newest.set(timestamp_newest),
            ]
        )


if __name__ == "__main__":
    fire.Fire(ETLOHLCVCommandLineInterface)
