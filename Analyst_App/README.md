# Analyst App

## Overview

The Analyst App is a robust and scalable solution designed for monitoring on-chain metrics of the Orchid (OXT) token. It provides real-time and historical insights into key performance indicators such as network activity, provider statistics, and transaction volumes. The application is built with a focus on clean architecture, testability, and maintainability, making it suitable for production environments.

### Key Features:

*   **Data Ingestion**: Periodically fetches OXT on-chain data from external APIs (e.g., CoinGecko).
*   **Data Storage**: Persists raw and processed on-chain data in a PostgreSQL database.
*   **API Endpoints**: Exposes RESTful APIs for data ingestion and retrieval of OXT metrics.
*   **Clean Architecture**: Structured into Domain, Application, Infrastructure, and Presentation layers for clear separation of concerns.
*   **Asynchronous Operations**: Leverages `asyncio` and `httpx` for efficient non-blocking I/O.
*   **Comprehensive Logging**: Configurable logging with different levels for better observability.
*   **Automated Documentation**: FastAPI automatically generates interactive API documentation.

## Architecture

The application follows a client-server architecture based on the principles of Clean Architecture:

*   **Server (FastAPI)**: The backend service responsible for data ingestion, processing, storage, and exposing API endpoints.
    *   **Core**: Contains shared utilities like logging configuration and application settings.
    *   **Domain**: Defines the core business logic and entities (e.g., `OXTMetric`, `OXTProvider`) and abstract repository interfaces.
    *   **Application**: Implements use cases (business rules specific to the application) that orchestrate interactions between the Domain and Infrastructure layers.
    *   **Infrastructure**: Handles external concerns such as database interactions (SQLAlchemy with PostgreSQL), external API calls (CoinGecko), and potentially caching (Redis).
    *   **Presentation**: The FastAPI layer that exposes API endpoints, handles request validation, and serializes responses.
*   **Client (Streamlit)**: (Planned) The frontend application for visualizing the OXT on-chain metrics.

## Getting Started

### Prerequisites

*   Python 3.10+
*   Poetry (recommended for dependency management) or `pip`
*   PostgreSQL database instance

### Setup

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd Analyst_App
    ```

2.  **Create a virtual environment and install dependencies:**
    ```bash
    # Using Poetry (recommended)
    poetry install
    poetry shell

    # Or using pip
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    pip install -r server/requirements.txt
    pip install -r client/requirements.txt # For client dependencies, if running client locally
    ```

3.  **Configure Environment Variables:**
    Create a `.env` file in the `Analyst_App/server/` directory with your database connection string and other settings:
    ```dotenv
    DATABASE_URL="postgresql+psycopg2://user:password@host:port/database_name"
    COINGECKO_API_BASE_URL="https://api.coingecko.com/api/v3"
    REDIS_URL="redis://localhost:6379/0"
    ```
    *Replace placeholders with your actual database credentials.*

### Running the Server (Local)

1.  **Navigate to the server directory:**
    ```bash
    cd Analyst_App/server
    ```

2.  **Run the FastAPI application:**
    ```bash
    uvicorn main:app --reload
    ```
    The server will start, and it will automatically create the necessary database tables on startup if they don't exist.

3.  **Access API Documentation:**
    Once the server is running, you can access the interactive OpenAPI documentation at `http://127.0.0.1:8000/docs` or `http://127.0.0.1:8000/redoc`.

### Running with Docker

1.  **Ensure Docker is installed and running.**

2.  **Navigate to the project root directory:**
    ```bash
    cd Analyst_App
    ```

3.  **Build and run the Docker containers:**
    ```bash
    docker-compose up --build
    ```
    This will build the server image, start the PostgreSQL database, Redis, and the FastAPI server. The database tables will be automatically created on server startup.

4.  **Access API Documentation:**
    Once the containers are running, you can access the interactive OpenAPI documentation at `http://localhost:8000/docs` or `http://localhost:8000/redoc`.

5.  **To stop the containers:**
    ```bash
    docker-compose down
    ```

### Running the Client (Planned)

*(Instructions for running the Streamlit client will be added here once implemented.)*

## API Endpoints

### Health Check

*   `GET /ping`
    *   **Description**: Checks the status of the CoinGecko API.
    *   **Response**: `{"gecko_says": "(V3) SimpleAPI is working!"}`

### Data Ingestion

*   `POST /api/v1/data/ingest/oxt`
    *   **Description**: Fetches historical OXT market data (prices, market caps, volumes) from CoinGecko and stores it in the database.
    *   **Response**: `{"status": "OXT metrics ingested successfully"}`

### OXT Metrics Retrieval (Planned)

*(Endpoints for retrieving stored OXT metrics will be added here.)*

## Development Guidelines

### Project Structure

```
Analyst_App/
├── server/
│   ├── main.py                 # FastAPI application entry point
│   ├── core/                   # Core utilities (logging, config)
│   │   ├── __init__.py
│   │   ├── config.py
│   │   └── logging_config.py
│   ├── domain/                 # Business logic and entities
│   │   ├── __init__.py
│   │   ├── models.py           # Pydantic domain models
│   │   └── repositories.py     # Abstract repository interfaces
│   ├── application/            # Application-specific use cases
│   │   ├── __init__.py
│   │   ├── services.py
│   │   └── use_cases.py
│   ├── infrastructure/         # External concerns (DB, external APIs)
│   │   ├── __init__.py
│   │   ├── database/           # SQLAlchemy ORM, DB connection
│   │   │   ├── __init__.py
│   │   │   ├── database.py
│   │   │   ├── models.py
│   │   │   └── repositories.py
│   │   └── external_apis/      # CoinGecko API client
│   │       ├── __init__.py
│   │       └── coingecko.py
│   ├── presentation/           # API endpoints (FastAPI routers)
│   │   └── __init__.py
│   ├── requirements.txt
│   └── .env.example
├── client/                     # Streamlit frontend (planned)
│   ├── main.py
│   └── requirements.txt
└── PRD.md
```

### Code Quality

*   **Type Hinting**: All new code should include comprehensive type hints.
*   **Linting & Formatting**: `ruff` and `black` are used for code quality and formatting. Ensure your IDE is configured to use them or run manually:
    ```bash
    ruff check .
    black .
    ```
*   **Testing**: Write unit and integration tests for new features.

### Logging

Structured logging is configured to provide clear insights into application behavior. Use the standard Python `logging` module with appropriate levels (`DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`).

## Contributing

Contributions are welcome! Please refer to the `PRD.md` for the project's vision and requirements.
