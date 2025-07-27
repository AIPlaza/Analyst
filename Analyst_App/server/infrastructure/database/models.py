from datetime import datetime
from uuid import uuid4

from sqlalchemy import Column, DateTime, Enum, Float, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base

from domain.models import MetricType, ProviderStatus

Base = declarative_base()


class OXTMetricORM(Base):
    __tablename__ = "oxt_metrics"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    metric_type = Column(Enum(MetricType), nullable=False)
    timestamp = Column(DateTime, nullable=False, default=datetime.utcnow)
    value = Column(Float, nullable=False)
    unit = Column(String, nullable=False)
    source = Column(String, nullable=False)


class OXTProviderORM(Base):
    __tablename__ = "oxt_providers"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    address = Column(String, nullable=False, unique=True)
    status = Column(Enum(ProviderStatus), nullable=False)
    last_seen = Column(DateTime, nullable=False, default=datetime.utcnow)
    stake_amount = Column(Float, nullable=False)
