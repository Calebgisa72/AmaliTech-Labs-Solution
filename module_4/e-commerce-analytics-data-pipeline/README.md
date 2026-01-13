# E-Commerce Analytics Data Pipeline

## 📌 Overview

The **E-Commerce Analytics Data Pipeline** is a lab designed to simulate a real-world data engineering scenario. It focuses on building a robust system that handles transactional operations, utilizes caching for performance, manages user sessions via NoSQL, and executes complex analytical queries for business intelligence.

**Key Objectives:**

- **Database Design**: Implement a normalized 3NF PostgreSQL schema.
- **Polyglot Persistence**: Integrate PostgreSQL (Relational), Redis (Cache), and MongoDB (Document Store).
- **Performance Optimization**: Use indexes and `EXPLAIN ANALYZE` to optimize query performance.
- **Analytics**: Write advanced SQL queries using Window Functions and Common Table Expressions (CTEs).

## 🏗️ Architecture

The system follows a modular architecture:

- **Core Database (PostgreSQL)**: Stores critical business data (Customers, Products, Orders).
- **Caching Layer (Redis)**: Caches high-traffic read operations (e.g., "Top Selling Products").
- **Session Store (MongoDB)**: Manages unstructured temporary data like shopping carts.
- **Application Logic (Python)**:
  - `src/services`: Business logic for handling orders and products.
  - `src/pipelines`: Data ingestion and transformation routines.
  - `src/analytics`: Complex reporting queries.

> For a detailed deep-dive into the system architecture and data flow, please refer to the [Architecture Documentation](docs/architecture.md).

## 🚀 Getting Started

### Prerequisites

Ensure you have the following installed on your local machine:

- **Python 3.11+**: [Download Here](https://www.python.org/downloads/)
- **Poetry** (Dependency Manager): [Installation Guide](https://python-poetry.org/docs/#installation)
- **PostgreSQL**: Local instance running on port `5432`.
- **Redis**: Local instance or Memurai (on Windows) running on port `6379`.
- **MongoDB**: Local instance running on port `27017`.

### ⚙️ Installation & Setup

1.  **Navigate to the Lab Directory**:

    ```bash
    cd module_4/e-commerce-analytics-data-pipeline
    ```

2.  **Install Dependencies**:
    Use Poetry to install all required libraries in a virtual environment.

    ```bash
    poetry install
    ```

3.  **Environment Configuration**:

    - Copy the example environment file:
      ```bash
      cp .env.example .env
      # On Windows Command Prompt: copy .env.example .env
      ```
    - Open `.env` and configure your local database credentials:
      ```ini
      POSTGRES_USER=your_postgres_user
      POSTGRES_PASSWORD=your_postgres_password
      POSTGRES_DB=ecommerce_db
      # ... other configurations
      ```

4.  **Activate Shell**:
    ```bash
    poetry shell
    ```

### 🏃 Running the Application

_Currently, the application consists of foundational services and models. Specific execution scripts for seeding data and running pipelines will be implemented in subsequent phases._

**Verifying the Setup:**
You can run the verification script to ensure all connections and dependencies are correctly configured:

```bash
python verify_setup.py
```

_(Note: Ensure `verify_setup.py` exists or create a simple script to test imports based on `src` structure)_

## 📂 Project Structure

```text
module_4/e-commerce-analytics-data-pipeline/
├── src/
│   ├── analytics/       # Analytical SQL queries & Reports
│   ├── config/          # Configuration management (settings.py)
│   ├── database/        # Connection handlers for Postgres, Redis, Mongo
│   ├── models/          # Data classes (Customer, Product, Order)
│   ├── pipelines/       # ETL scripts (Ingestion, Transformation)
│   ├── services/        # Business logic services
│   └── utils/           # Shared utilities (logging, helpers)
├── docs/                # Documentation
├── tests/               # Unit and Integration tests
├── .env                 # Local environment variables
└── pyproject.toml       # Project dependencies
```

## 🧪 Testing

To run the test suite (once implemented):

```bash
pytest
```

## 📝 License

This project is part of the AmaliTech Lab Solutions.
