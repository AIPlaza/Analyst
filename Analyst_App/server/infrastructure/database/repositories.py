from datetime import datetime
from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm import Session

from domain.models import OXTMetric, OXTProvider, MetricType, ProviderStatus
from domain.repositories import IOXTMetricRepository, IOXTProviderRepository
from infrastructure.database.models import OXTMetricORM, OXTProviderORM


class OXTMetricRepository(IOXTMetricRepository):
    def __init__(self, db: Session):
        self.db = db

    def add(self, metric: OXTMetric) -> OXTMetric:
        db_metric = OXTMetricORM(**metric.model_dump())
        self.db.add(db_metric)
        self.db.commit()
        self.db.refresh(db_metric)
        return OXTMetric.model_validate(db_metric)

    def get_by_id(self, metric_id: UUID) -> Optional[OXTMetric]:
        db_metric = self.db.query(OXTMetricORM).filter(OXTMetricORM.id == metric_id).first()
        if db_metric:
            return OXTMetric.model_validate(db_metric)
        return None

    def get_metrics(self, metric_type: Optional[str] = None, start_date: Optional[datetime] = None, end_date: Optional[datetime] = None) -> List[OXTMetric]:
        query = self.db.query(OXTMetricORM)
        if metric_type:
            query = query.filter(OXTMetricORM.metric_type == MetricType(metric_type))
        if start_date:
            query = query.filter(OXTMetricORM.timestamp >= start_date)
        if end_date:
            query = query.filter(OXTMetricORM.timestamp <= end_date)
        return [OXTMetric.model_validate(metric) for metric in query.all()]


class OXTProviderRepository(IOXTProviderRepository):
    def __init__(self, db: Session):
        self.db = db

    def add(self, provider: OXTProvider) -> OXTProvider:
        db_provider = OXTProviderORM(**provider.model_dump())
        self.db.add(db_provider)
        self.db.commit()
        self.db.refresh(db_provider)
        return OXTProvider.model_validate(db_provider)

    def get_by_id(self, provider_id: UUID) -> Optional[OXTProvider]:
        db_provider = self.db.query(OXTProviderORM).filter(OXTProviderORM.id == provider_id).first()
        if db_provider:
            return OXTProvider.model_validate(db_provider)
        return None

    def get_by_address(self, address: str) -> Optional[OXTProvider]:
        db_provider = self.db.query(OXTProviderORM).filter(OXTProviderORM.address == address).first()
        if db_provider:
            return OXTProvider.model_validate(db_provider)
        return None

    def get_all(self) -> List[OXTProvider]:
        return [OXTProvider.model_validate(provider) for provider in self.db.query(OXTProviderORM).all()]

    def update(self, provider: OXTProvider) -> OXTProvider:
        db_provider = self.db.query(OXTProviderORM).filter(OXTProviderORM.id == provider.id).first()
        if db_provider:
            for key, value in provider.model_dump(exclude_unset=True).items():
                setattr(db_provider, key, value)
            self.db.commit()
            self.db.refresh(db_provider)
            return OXTProvider.model_validate(db_provider)
        raise ValueError(f"Provider with ID {provider.id} not found.")
