import requests
import json
import csv
import logging
from datetime import datetime
from sqlalchemy.orm import Session

from app.db import SessionLocal
from app.schemas import (
    CryptoAsset,
    CryptoPrice,
    RawData,
    ETLCheckpoint,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("app.ingestion")

COINPAPRIKA_URL = "https://api.coinpaprika.com/v1/tickers"


def get_checkpoint(db: Session, source: str):
    return db.query(ETLCheckpoint).filter_by(source=source).first()


def update_checkpoint(db: Session, source: str):
    checkpoint = get_checkpoint(db, source)
    if checkpoint:
        checkpoint.last_run = datetime.utcnow()
    else:
        db.add(ETLCheckpoint(source=source, last_run=datetime.utcnow()))


def get_or_create_asset(db: Session, symbol: str, name: str) -> CryptoAsset:
    asset = db.query(CryptoAsset).filter_by(symbol=symbol).first()
    if not asset:
        asset = CryptoAsset(symbol=symbol, name=name)
        db.add(asset)
        db.flush()
    return asset


def ingest_coinpaprika():
    logger.info("Starting CoinPaprika ingestion")
    db = SessionLocal()

    try:
        response = requests.get(COINPAPRIKA_URL, timeout=10)
        response.raise_for_status()
        data = response.json()

        for item in data[:10]:
            db.add(RawData(
                source="coinpaprika",
                payload=json.dumps(item),
            ))

            asset = get_or_create_asset(
                db,
                symbol=item["symbol"],
                name=item["name"],
            )

            price = (
                db.query(CryptoPrice)
                .filter_by(asset_id=asset.id, source="coinpaprika")
                .first()
            )

            if price:
                price.price_usd = item["quotes"]["USD"]["price"]
                price.fetched_at = datetime.utcnow()
            else:
                db.add(CryptoPrice(
                    asset_id=asset.id,
                    source="coinpaprika",
                    price_usd=item["quotes"]["USD"]["price"],
                ))

        update_checkpoint(db, "coinpaprika")
        db.commit()
        logger.info("CoinPaprika ingestion completed")

    except Exception:
        db.rollback()
        logger.exception("CoinPaprika ingestion failed")
        raise
    finally:
        db.close()


def ingest_csv():
    logger.info("Starting CSV ingestion")
    db = SessionLocal()

    checkpoint = get_checkpoint(db, "csv")
    if checkpoint:
        logger.info("CSV already ingested, skipping")
        db.close()
        return

    try:
        with open("data/crypto_prices.csv") as f:
            reader = csv.DictReader(f)

            for row in reader:
                db.add(RawData(
                    source="csv",
                    payload=json.dumps(row),
                ))

                asset = get_or_create_asset(
                    db,
                    symbol=row["symbol"],
                    name=row["name"],
                )

                db.add(CryptoPrice(
                    asset_id=asset.id,
                    source="csv",
                    price_usd=float(row["price_usd"]),
                ))

        update_checkpoint(db, "csv")
        db.commit()
        logger.info("CSV ingestion completed")

    except Exception:
        db.rollback()
        logger.exception("CSV ingestion failed")
        raise
    finally:
        db.close()
