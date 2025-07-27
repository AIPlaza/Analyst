# Product Requirements Document: Analyst App

## 1. Introduction

The Analyst App is designed to provide a robust and scalable solution for monitoring on-chain metrics of the Orchid (OXT) token. This application aims to deliver real-time and historical insights into network activity, provider statistics, and transaction volumes, enabling comprehensive analysis for researchers, investors, and OXT holders.

## 2. Functional Requirements

### 2.1 Data Ingestion
- **FR1.1:** The system shall periodically fetch OXT on-chain data from reliable external APIs (e.g., CoinGecko, Etherscan, or other specialized blockchain data providers).
- **FR1.2:** The system shall support configurable data fetching intervals.
- **FR1.3:** The system shall handle API rate limits and implement appropriate retry mechanisms.
- **FR1.4:** The system shall store raw and processed on-chain data in a persistent database.

### 2.2 Data Processing & Analysis
- **FR2.1:** The system shall process raw data to derive key metrics:
    - Network Activity (e.g., daily active addresses, total transactions).
    - Number of Providers (e.g., active OXT stakers/nodes).
    - Transaction Volume (e.g., 24-hour volume, historical volume).
- **FR2.2:** The system shall aggregate data over various timeframes (e.g., daily, weekly, monthly).

### 2.3 API Endpoints (Server)
- **FR3.1:** The server shall expose RESTful API endpoints for retrieving processed OXT metrics.
- **FR3.2:** Endpoints shall support filtering by time range and specific metric types.
- **FR3.3:** Example Endpoints:
    - `GET /api/v1/oxt/metrics/network-activity?start_date=<date>&end_date=<date>`
    - `GET /api/v1/oxt/metrics/providers?date=<date>`
    - `GET /api/v1/oxt/metrics/transaction-volume?start_date=<date>&end_date=<date>`
    - `POST /api/v1/data/ingest/oxt` (Trigger manual data ingestion for OXT)
    - `GET /health` (Health check endpoint)

### 2.4 User Interface (Client)
- **FR4.1:** The client shall provide a dashboard to visualize OXT on-chain metrics.
- **FR4.2:** The dashboard shall display interactive charts for trends over time.
- **FR4.3:** Users shall be able to select time ranges for data visualization.
- **FR4.4:** The client shall display current key metrics (e.g., latest active providers count).

## 3. Non-Functional Requirements

### 3.1 Performance
- **NFR3.1.1:** API response times for metric retrieval shall be under 200ms for typical queries.
- **NFR3.1.2:** Data ingestion processes shall complete within acceptable windows (e.g., daily ingestion within 1 hour).

### 3.2 Scalability
- **NFR3.2.1:** The server architecture shall support horizontal scaling to handle increased API requests.
- **NFR3.2.2:** The database schema and queries shall be optimized for large datasets.

### 3.3 Reliability & Availability
- **NFR3.3.1:** The system shall have a high availability target (e.g., 99.9%).
- **NFR3.3.2:** Error handling shall be robust, with appropriate logging and graceful degradation.
- **NFR3.3.3:** External API calls shall implement circuit breakers and retry logic.

### 3.4 Security
- **NFR3.4.1:** API keys for external services shall be securely managed (e.g., environment variables, secret management).
- **NFR3.4.2:** Data stored in the database shall be protected against unauthorized access.

### 3.5 Maintainability
- **NFR3.5.1:** Codebase shall adhere to Python best practices (PEP 8) and be well-documented.
- **NFR3.5.2:** Clear separation of concerns through layered architecture.
- **NFR3.5.3:** Comprehensive unit and integration tests shall be provided.

### 3.6 Observability
- **NFR3.6.1:** The system shall implement structured logging with configurable levels (DEBUG, INFO, WARNING, ERROR, CRITICAL).
- **NFR3.6.2:** Key metrics (e.g., API call success/failure rates, data ingestion duration) shall be exposed for monitoring.

### 3.7 Deployment
- **NFR3.7.1:** The application shall be containerized using Docker for consistent deployment environments.
- **NFR3.7.2:** Deployment process shall be automated (CI/CD friendly).

## 4. Technical Architecture

The application will follow a clean, layered architecture to ensure separation of concerns, testability, and maintainability.

### 4.1 Layers

-   **Infrastructure Layer:**
    -   Handles external concerns: database interactions (PostgreSQL), external API calls (CoinGecko), caching (Redis), logging, and configuration management.
    -   Provides interfaces for the Application Layer.
-   **Domain Layer:**
    -   Contains the core business logic and entities (e.g., `OXTMetric`, `ProviderData`).
    -   Independent of external frameworks or databases.
    -   Defines domain services and repositories interfaces.
-   **Application Layer:**
    -   Orchestrates the Domain and Infrastructure layers to implement specific use cases (e.g., `FetchOXTMetricsUseCase`, `IngestOXTDataUseCase`).
    -   Contains application services and DTOs (Data Transfer Objects).
    -   Handles transaction management and security concerns.
-   **Presentation Layer (Server/Client):**
    -   **Server (FastAPI):** Exposes the API endpoints, handles request parsing, validation, and serialization of responses. Interacts with the Application Layer.
    -   **Client (Streamlit):** Provides the user interface, makes requests to the server API, and visualizes the data.

### 4.2 Technology Stack

-   **Server:**
    -   **Language:** Python 3.10+
    -   **Web Framework:** FastAPI
    -   **Database ORM:** SQLAlchemy 2.0
    -   **Database:** PostgreSQL
    -   **Data Validation:** Pydantic
    -   **HTTP Client:** `httpx` (for async requests) or `requests`
    -   **Caching:** Redis (via `redis-py`)
    -   **Dependency Management:** `pip` with `requirements.txt`
    -   **Type Hinting:** MyPy
    -   **Linting/Formatting:** Black, Ruff
    -   **Testing:** Pytest
    -   **Logging:** Standard Python `logging` module

-   **Client:**
    -   **Language:** Python 3.10+
    -   **Web Framework:** Streamlit
    -   **Data Visualization:** Plotly, Matplotlib
    -   **HTTP Client:** `requests`

## 5. Data Model (Conceptual)

-   **`OXTMetric`**: Represents a single on-chain metric data point.
    -   `id` (UUID)
    -   `metric_type` (Enum: `NETWORK_ACTIVITY`, `PROVIDERS`, `TRANSACTION_VOLUME`)
    -   `timestamp` (DateTime)
    -   `value` (Float/Decimal)
    -   `unit` (String, e.g., "count", "USD")
    -   `source` (String, e.g., "CoinGecko", "Etherscan")
-   **`OXTProvider`**: Represents a provider/node on the Orchid network.
    -   `id` (UUID)
    -   `address` (String)
    -   `status` (Enum: `ACTIVE`, `INACTIVE`)
    -   `last_seen` (DateTime)
    -   `stake_amount` (Decimal)

*(Note: This is a conceptual model. Detailed schema will be defined during implementation.)*

## 6. API Design

-   **Versioning:** `/api/v1/` prefix for all endpoints.
-   **Authentication:** Initially, no authentication. For production, consider API key or OAuth2.
-   **Error Handling:** Standard HTTP status codes (400, 404, 500) with JSON error responses.
    ```json
    {
        "detail": "Error message describing the issue."
    }
    ```
-   **Request/Response Formats:** JSON.

## 7. Client Design

-   **Dashboard Layout:** Clear, intuitive layout with sections for each metric type.
-   **Interactivity:** Date pickers, dropdowns for metric selection.
-   **Visualizations:** Line charts for time-series data, bar charts for comparisons.

## 8. Development & Deployment Considerations

### 8.1 Development Environment
-   Use `venv` for isolated Python environments.
-   `requirements.txt` for strict dependency management.
-   Pre-commit hooks for linting and formatting.

### 8.2 Testing
-   **Unit Tests:** Cover individual functions and classes (Domain, Application layers).
-   **Integration Tests:** Verify interactions between layers (e.g., API to Application, Application to Database).
-   **End-to-End Tests:** Simulate user flows (Client to Server to Database).

### 8.3 Logging
-   Centralized logging configuration.
-   Use `logger.info()`, `logger.warning()`, `logger.error()`, `logger.debug()` appropriately.
-   Log format: JSON for easier parsing by log aggregators.

### 8.4 Configuration
-   Environment variables for sensitive information (database credentials, API keys).
-   Configuration files for non-sensitive settings.

### 8.5 CI/CD
-   Automated testing on every push.
-   Automated Docker image build and push.
-   Automated deployment to staging/production environments.

### 8.6 `__MACOSX` Folder
-   This folder is a macOS-specific artifact from archiving. It will be ignored in `.gitignore` and will not be part of the deployed application.

---
**End of PRD**
