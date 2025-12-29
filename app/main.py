from fastapi import FastAPI
import time
import uuid
from app.schemas import Base, CryptoAsset, RawData, ETLCheckpoint
from sqlalchemy.orm import joinedload

from app.db import engine, SessionLocal
from app.schemas import Base, CryptoAsset
from app.ingestion import ingest_coinpaprika, ingest_csv



app = FastAPI(title="Kasparro Backend")

@app.on_event("startup")
def startup_event():
    ingest_coinpaprika()
    ingest_csv() 

@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "database": "connected",
        "timestamp": time.time(),
        "request_id": str(uuid.uuid4())
    }

@app.get("/data")
def get_data(limit: int = 10, offset: int = 0):
    start_time = time.time()
    request_id = str(uuid.uuid4())

    db = SessionLocal()

    assets = (
        db.query(CryptoAsset)
        .options(joinedload(CryptoAsset.prices))
        .offset(offset)
        .limit(limit)
        .all()
    )

    result = []
    for a in assets:
        # Get latest price for that asset
        latest_price = (
            sorted(a.prices, key=lambda p: p.fetched_at or 0, reverse=True)[0].price_usd
            if a.prices else None
        )

        result.append({
            "symbol": a.symbol,
            "name": a.name,
            "latest_price_usd": latest_price,
        })

    db.close()
    latency_ms = int((time.time() - start_time) * 1000)

    return {
        "request_id": request_id,
        "api_latency_ms": latency_ms,
        "count": len(result),
        "data": result
    }

@app.get("/stats")
def get_stats():
    db = SessionLocal()

    raw_count = db.query(RawData).count()
    asset_count = db.query(CryptoAsset).count()
    checkpoints = db.query(ETLCheckpoint).all()

    db.close()

    return {
        "raw_records": raw_count,
        "normalized_records": asset_count,
        "sources": [
            {
                "source": c.source,
                "last_run": c.last_run
            }
            for c in checkpoints
        ]
    }
