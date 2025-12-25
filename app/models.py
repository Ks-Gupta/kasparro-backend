from sqlalchemy import Column, Integer, String, Float, DateTime
from app.db import Base

class CryptoAsset(Base):
    __tablename__ = "crypto_assets"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String)
    name = Column(String)
    price_usd = Column(Float)
    