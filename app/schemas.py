from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, UniqueConstraint
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

Base = declarative_base()


class CryptoAsset(Base):
    __tablename__ = "crypto_assets"

    id = Column(Integer, primary_key=True)
    symbol = Column(String(20), nullable=False, unique=True)
    name = Column(String(100), nullable=False)

    prices = relationship("CryptoPrice", back_populates="asset")


class CryptoPrice(Base):
    __tablename__ = "crypto_prices"
    __table_args__ = (
        UniqueConstraint("asset_id", "source", name="uq_asset_source"),
    )

    id = Column(Integer, primary_key=True)
    asset_id = Column(Integer, ForeignKey("crypto_assets.id"))
    source = Column(String(50), nullable=False)
    price_usd = Column(Float, nullable=False)
    fetched_at = Column(DateTime, default=datetime.utcnow)

    asset = relationship("CryptoAsset", back_populates="prices")


class RawData(Base):
    __tablename__ = "raw_data"

    id = Column(Integer, primary_key=True)
    source = Column(String(50), nullable=False)
    payload = Column(Text, nullable=False)
    ingested_at = Column(DateTime, default=datetime.utcnow)


class ETLCheckpoint(Base):
    __tablename__ = "etl_checkpoints"

    id = Column(Integer, primary_key=True)
    source = Column(String(50), nullable=False, unique=True)
    last_run = Column(DateTime)
