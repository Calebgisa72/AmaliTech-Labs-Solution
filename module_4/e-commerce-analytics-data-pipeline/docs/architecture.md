# E-Commerce Analytics Data Pipeline - Architecture

## Overview

This project involves building a robust data processing and analytics pipeline for a fictional e-commerce store. It simulates a real-world scenario where transactional data processing, caching, session management, and complex analytics are integrated into a single system.

## Architecture

The system utilizes a polyglot persistence architecture:

1.  **PostgreSQL (Relational Core)**: Stores the primary business entities (Customers, Products, Orders, Order Items) in a normalized 3NF schema. It also leverages `JSONB` for flexible product metadata.
2.  **Redis (Caching Layer)**: Acts as a high-speed cache for read-heavy operations, such as retrieving "Top 10 Best-Selling Products".
3.  **MongoDB (Session Store)**: generic store for unstructured data like user shopping carts before order finalization.

### Data Flow

1.  **Ingestion/Transactional**: Python scripts process new orders.
    - Validate stock (Postgres).
    - Create Order (Postgres Transaction).
    - Clear Cart (Mongo).
    - Update Cache (Redis - invalidation/write-through).
2.  **Analytics**: Complex SQL queries run against Postgres to generate reports. Performance is optimized using Indexes and analyzed via `EXPLAIN ANALYZE`.

## Tech Stack

- **Language**: Python 3.11+
- **Database**: PostgreSQL 15+ (Local Instance)
- **NoSQL**: Redis (Stack), MongoDB (Local Instances)
- **Dependency Management**: Poetry

## Project Structure

```
module_4/e-commerce-analytics-data-pipeline/
├── src/
│   ├── analytics/       # SQL queries, window functions, CTEs
│   ├── config/          # Configuration and env var loading
│   ├── database/        # DB connections (Postgres, Redis, Mongo) & DDL
│   ├── models/          # Python data classes for domain entities
│   ├── services/        # Business logic (Order processing, etc.)
│   └── utils/           # Helper functions
├── docs/
│   └── architecture.md  # This file
├── tests/               # Unit and integration tests
├── .env                 # Environment variables (git-ignored)
├── pyproject.toml       # Python dependencies
└── README.md            # (To be added in final phase)
```

## Setup Instructions

### Prerequisites

- Python 3.11+ installed.
- Poetry installed.
- **Local Databases**: Ensure PostgreSQL, Redis, and MongoDB are installed and running locally.

### Installation

1.  **Clone the repository** (if not already local).
2.  **Install Dependencies**:
    ```bash
    poetry install
    ```
3.  **Activate Virtual Environment**:
    ```bash
    source $(poetry env info --path)/bin/activate  # Linux/Mac
    # OR
    .\venv\Scripts\activate                        # Windows
    ```

## Usage

_Instructions for running specific scripts will be added in Phase 2._
