from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional
from uuid import UUID

from domain.models import OXTMetric, OXTProvider


class IOXTMetricRepository(ABC):
    @abstractmethod
    def add(self, metric: OXTMetric) -> OXTMetric:
        pass

    @abstractmethod
    def get_by_id(self, metric_id: UUID) -> Optional[OXTMetric]:
        pass

    @abstractmethod
    def get_metrics(self, metric_type: Optional[str] = None, start_date: Optional[datetime] = None, end_date: Optional[datetime] = None) -> List[OXTMetric]:
        pass


class IOXTProviderRepository(ABC):
    @abstractmethod
    def add(self, provider: OXTProvider) -> OXTProvider:
        pass

    @abstractmethod
    def get_by_id(self, provider_id: UUID) -> Optional[OXTProvider]:
        pass

    @abstractmethod
    def get_by_address(self, address: str) -> Optional[OXTProvider]:
        pass

    @abstractmethod
    def get_all(self) -> List[OXTProvider]:
        pass

    @abstractmethod
    def update(self, provider: OXTProvider) -> OXTProvider:
        pass