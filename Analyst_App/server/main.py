print("Server application starting...")
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, Query, status, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
import logging

from core.logging_config import setup_logging
from core.exceptions import NotFoundException, ExternalAPIError, DatabaseError, InvalidInputException
from application.use_cases import PingCoinGeckoUseCase, IngestOXTMetricsUseCase, GetOXTMetricsUseCase
from infrastructure.database.database import create_db_and_tables, get_db
from infrastructure.database.repositories import OXTMetricRepository
from domain.models import OXTMetric, MetricType

setup_logging()
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Application startup event triggered.")
    create_db_and_tables()
    logger.info("Database tables created/checked.")
    yield
    logger.info("Application shutdown event triggered.")

app = FastAPI(
    title="Analyst App Server API",
    description="API for fetching on-chain data for the Orchid token (OXT).",
    lifespan=lifespan
)

@app.exception_handler(NotFoundException)
async def not_found_exception_handler(request: Request, exc: NotFoundException):
    logger.warning(f"NotFoundException: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )

@app.exception_handler(ExternalAPIError)
async def external_api_error_handler(request: Request, exc: ExternalAPIError):
    logger.error(f"ExternalAPIError: {exc.detail}", exc_info=True)
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )

@app.exception_handler(DatabaseError)
async def database_error_handler(request: Request, exc: DatabaseError):
    logger.error(f"DatabaseError: {exc.detail}", exc_info=True)
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )

@app.exception_handler(InvalidInputException)
async def invalid_input_exception_handler(request: Request, exc: InvalidInputException):
    logger.warning(f"InvalidInputException: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )

@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    logger.exception(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "An unexpected error occurred."},
    )

@app.get("/", summary="Root endpoint", description="Returns a simple greeting message.")
def read_root():
    return {"Hello": "World"}

@app.get("/ping", summary="Ping CoinGecko API", description="Checks the status of the CoinGecko API.")
async def ping():
    try:
        use_case = PingCoinGeckoUseCase()
        result = await use_case.execute()
        logger.info("CoinGecko ping successful.")
        return result
    except Exception as e:
        logger.error(f"Error pinging CoinGecko: {e}", exc_info=True)
        raise ExternalAPIError(detail="Failed to ping CoinGecko API")

@app.post("/api/v1/data/ingest/oxt", summary="Ingest OXT Metrics", description="Fetches and stores OXT on-chain metrics from CoinGecko.")
async def ingest_oxt_metrics(db: Session = Depends(get_db)):
    try:
        metric_repo = OXTMetricRepository(db)
        use_case = IngestOXTMetricsUseCase(metric_repo)
        result = await use_case.execute()
        logger.info("OXT metrics ingestion successful.")
        return result
    except Exception as e:
        logger.error(f"Error ingesting OXT metrics: {e}", exc_info=True)
        raise DatabaseError(detail="Failed to ingest OXT metrics")

@app.get("/api/v1/oxt/metrics", response_model=List[OXTMetric], summary="Get OXT Metrics", description="Retrieves stored OXT on-chain metrics, with optional filtering.")
async def get_oxt_metrics(
    metric_type: Optional[MetricType] = Query(None, description="Filter by metric type (e.g., network_activity, providers, transaction_volume)"),
    start_date: Optional[datetime] = Query(None, description="Filter by start date (YYYY-MM-DDTHH:MM:SS)"),
    end_date: Optional[datetime] = Query(None, description="Filter by end date (YYYY-MM-DDTHH:MM:SS)"),
    db: Session = Depends(get_db)
) -> List[OXTMetric]:
    try:
        metric_repo = OXTMetricRepository(db)
        use_case = GetOXTMetricsUseCase(metric_repo)
        metrics = use_case.execute(metric_type, start_date, end_date)
        logger.info(f"Retrieved {len(metrics)} OXT metrics.")
        return metrics
    except Exception as e:
        logger.error(f"Error retrieving OXT metrics: {e}", exc_info=True)
        raise DatabaseError(detail="Failed to retrieve OXT metrics")
