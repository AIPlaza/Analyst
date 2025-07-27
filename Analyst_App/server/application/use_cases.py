from infrastructure.external_apis.coingecko import ping as coingecko_ping, get_oxt_market_chart
from domain.repositories import IOXTMetricRepository
from domain.models import OXTMetric, MetricType
from datetime import datetime
from typing import List, Optional

class PingCoinGeckoUseCase:
    async def execute(self):
        return await coingecko_ping()

class IngestOXTMetricsUseCase:
    def __init__(self, metric_repository: IOXTMetricRepository):
        self.metric_repository = metric_repository

    async def execute(self):
        market_data = await get_oxt_market_chart()

        # Ingest prices
        for timestamp, value in market_data.get("prices", []):
            metric = OXTMetric(
                metric_type=MetricType.NETWORK_ACTIVITY, # Using NETWORK_ACTIVITY for price for now, will refine later
                timestamp=datetime.fromtimestamp(timestamp / 1000),
                value=value,
                unit="USD",
                source="CoinGecko"
            )
            self.metric_repository.add(metric)

        # Ingest market caps
        for timestamp, value in market_data.get("market_caps", []):
            metric = OXTMetric(
                metric_type=MetricType.TRANSACTION_VOLUME, # Using TRANSACTION_VOLUME for market cap for now, will refine later
                timestamp=datetime.fromtimestamp(timestamp / 1000),
                value=value,
                unit="USD",
                source="CoinGecko"
            )
            self.metric_repository.add(metric)

        # Ingest total volumes
        for timestamp, value in market_data.get("total_volumes", []):
            metric = OXTMetric(
                metric_type=MetricType.TRANSACTION_VOLUME, # Using TRANSACTION_VOLUME for total volume for now, will refine later
                timestamp=datetime.fromtimestamp(timestamp / 1000),
                value=value,
                unit="USD",
                source="CoinGecko"
            )
            self.metric_repository.add(metric)

        return {"status": "OXT metrics ingested successfully"}


class GetOXTMetricsUseCase:
    def __init__(self, metric_repository: IOXTMetricRepository):
        self.metric_repository = metric_repository

    def execute(self, metric_type: Optional[MetricType] = None, start_date: Optional[datetime] = None, end_date: Optional[datetime] = None) -> List[OXTMetric]:
        return self.metric_repository.get_metrics(metric_type, start_date, end_date)
