from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()

class MarketData(Base):
    __tablename__ = 'market_data'

    id = Column(Integer, primary_key=True)
    symbol = Column(String, index=True)
    date = Column(DateTime, index=True)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    volume = Column(Float)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


class Trade(Base):
    __tablename__ = 'trades'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), index=True)
    market_data_id = Column(Integer, ForeignKey('market_data.id'), index=True)
    trade_date = Column(DateTime, index=True)
    trade_type = Column(String)
    quantity = Column(Float)
    price = Column(Float)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    market_data = relationship('MarketData')


class ModelPerformance(Base):
    __tablename__ = 'model_performance'

    id = Column(Integer, primary_key=True)
    model_name = Column(String, index=True)
    accuracy = Column(Float)
    precision = Column(Float)
    recall = Column(Float)
    f1_score = Column(Float)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


class Metrics(Base):
    __tablename__ = 'metrics'

    id = Column(Integer, primary_key=True)
    metric_name = Column(String, index=True)
    value = Column(Float)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


class Log(Base):
    __tablename__ = 'logs'

    id = Column(Integer, primary_key=True)
    log_message = Column(String)
    log_level = Column(String, index=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
