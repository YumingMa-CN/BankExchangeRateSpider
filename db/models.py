# --coding:UTF-8--
from sqlalchemy import Column, Integer, String, Numeric, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class ExchangeRate(Base):
    __tablename__ = "exchange_rate"
    id = Column(Integer, primary_key=True, autoincrement=True)
    currency_name = Column(String(32))
    currency_code = Column(String(8))
    base_amount = Column(Numeric(12,4))
    refer_price = Column(Numeric(16,6), nullable=True)
    remit_buy = Column(Numeric(16,6), nullable=True)
    cash_buy = Column(Numeric(16,6), nullable=True)
    remit_sell = Column(Numeric(16,6), nullable=True)
    cash_sell = Column(Numeric(16,6), nullable=True)
    mid_price = Column(Numeric(16,6), nullable=True)
    convert_price = Column(Numeric(16,6), nullable=True)
    update_time = Column(DateTime)
    crawl_time = Column(DateTime)
    bank = Column(String(32))
    ext_json = Column(JSON, nullable=True)
