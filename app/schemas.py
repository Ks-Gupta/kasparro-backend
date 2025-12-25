from sqlalchemy import Column, String, Float, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class RawData(Base):
    __tablename__ = "raw_data"

    id = Column(String, primary_key=True)
    source = Column(String)
    payload = Column(Text)
    ingested_at = Column(DateTime, default=datetime.utcnow)


class CryptoAsset(Base):
    __tablename__ = "crypto_assets"

    symbol = Column(String, primary_key=True)
    name = Column(String)
    price_usd = Column(Float)
    source = Column(String)
    updated_at = Column(DateTime, default=datetime.utcnow)

class ETLCheckpoint(Base):
    __tablename__ = "etl_checkpoint"

    source = Column(String, primary_key=True)
    last_run = Column(DateTime)
