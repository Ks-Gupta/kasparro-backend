import requests
import json
import uuid
from datetime import datetime

from app import db
from app.db import SessionLocal
from app.schemas import RawData, CryptoAsset
import logging
import csv
from app.schemas import ETLCheckpoint


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


COINPAPRIKA_URL = "https://api.coinpaprika.com/v1/tickers"

# CoinPaprika Ingestion
def ingest_coinpaprika():
    logger.info("Starting CoinPaprika ingestion...")


    response = requests.get(COINPAPRIKA_URL, timeout=10)
    response.raise_for_status()

    data = response.json()

    db = SessionLocal()

    for item in data[:10]:  # only 10 records (safe for beginners)
        raw = RawData(
            id=str(uuid.uuid4()),
            source="coinpaprika",
            payload=json.dumps(item),
            ingested_at=datetime.utcnow()
        )
        db.add(raw)

        asset = CryptoAsset(
            symbol=item.get("symbol"),
            name=item.get("name"),
            price_usd=item.get("quotes", {}).get("USD", {}).get("price", 0.0),
            source="coinpaprika",
            updated_at=datetime.utcnow()
        )
        db.merge(asset)  # idempotent write

    db.commit()
    db.close()

    logger.info("CoinPaprika ingestion completed.")

# CSV Ingestion
def ingest_csv():
    logger.info("Starting CSV ingestion...")

    db = SessionLocal()

    # 1️⃣ Check checkpoint
    last_run = get_last_run(db, "csv")
    if last_run:
        logger.info("CSV already ingested, skipping.")
        db.close()
        return

    # 2️⃣ Read CSV file
    with open("data/crypto_prices.csv", newline="") as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            # Store raw data
            raw = RawData(
                id=str(uuid.uuid4()),
                source="csv",
                payload=json.dumps(row),
                ingested_at=datetime.utcnow()
            )
            db.add(raw)

            # Normalize into unified schema
            asset = CryptoAsset(
                symbol=row["symbol"],
                name=row["name"],
                price_usd=float(row["price_usd"]),
                source="csv",
                updated_at=datetime.utcnow()
            )

            # Idempotent write (update if exists, insert if not)
            db.merge(asset)

    # 3️⃣ Update checkpoint AFTER successful ingestion
    update_last_run(db, "csv")

    db.commit()
    db.close()

    logger.info("CSV ingestion completed.")


# Helper functions for ETL checkpointing
def get_last_run(db, source: str):
    checkpoint = db.query(ETLCheckpoint).filter_by(source=source).first()
    return checkpoint.last_run if checkpoint else None


def update_last_run(db, source: str):
    checkpoint = db.query(ETLCheckpoint).filter_by(source=source).first()
    if checkpoint:
        checkpoint.last_run = datetime.utcnow()
    else:
        checkpoint = ETLCheckpoint(
            source=source,
            last_run=datetime.utcnow()
        )
        db.add(checkpoint)

