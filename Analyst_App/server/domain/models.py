from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, ConfigDict


class MetricType(str, Enum):
    NETWORK_ACTIVITY = "network_activity"
    PROVIDERS = "providers"
    TRANSACTION_VOLUME = "transaction_volume"


class ProviderStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"


class OXTMetric(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    metric_type: MetricType
    timestamp: datetime
    value: float
    unit: str
    source: str

    model_config = ConfigDict(from_attributes=True)


class OXTProvider(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    address: str
    status: ProviderStatus
    last_seen: datetime
    stake_amount: float

    model_config = ConfigDict(from_attributes=True)