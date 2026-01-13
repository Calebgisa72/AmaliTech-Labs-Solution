# E-Commerce Analytics Data Pipeline - Architecture

## 📖 Overview

This document provides a detailed technical overview of the E-Commerce Analytics Data Pipeline. The system is designed to demonstrate high-performance data processing patterns by integrating relational transaction processing with NoSQL capabilities.

## 🏗️ System Architecture

The solution implements a **Polyglot Persistence** architecture, leveraging the best tool for each specific data workload.

### 1. Relational Core (PostgreSQL)

- **Role**: Primary Source of Truth.
- **Data Models**:
  - `Customers`: User profiles.
  - `Products`: Catalog items with `JSONB` metadata for flexible attributes (colors, sizes).
  - `Orders` & `OrderItems`: Transactional records.
- **Key Features**:
  - ACID compliance for order placement.
  - Complex relational queries for analytics.

### 2. Caching Layer (Redis)

- **Role**: High-speed data retrieval.
- **Usage**:
  - Caching the results of expensive queries (e.g., "Top 10 Best Sellers").
  - TTL (Time-to-Live) strategies for automatic cache invalidation.

### 3. Session Store (MongoDB)

- **Role**: Temporary / Unstructured data storage.
- **Usage**:
  - `Shopping Cart`: Stores items added by users before checkout.
  - Allows high write throughput and flexible schema for session data.

---

## 🔄 Data Flow

### Order Processing Pipeline

1.  **User adds item to cart**: Data written to **MongoDB**.
2.  **User places order**:
    - App reads cart from MongoDB.
    - App starts **PostgreSQL Transaction**:
      - Deducts stock from `Products`.
      - Inserts record into `Orders` & `OrderItems`.
    - On success:
      - Cart is cleared from MongoDB.
      - **Redis** cache for product stock is invalidated/updated.

### Analytics Pipeline

1.  **Report Generation**:
    - Complex SQL (Window Functions, CTEs) executed against **PostgreSQL**.
2.  **Optimization**:
    - `EXPLAIN ANALYZE` used to identify bottlenecks.
    - Indexes (B-Tree, GIN) applied to optimize lookup and JSONB querying.

---

## 📂 Code Structure & Responsibilities

| Directory       | Component          | Responsibility                                          |
| :-------------- | :----------------- | :------------------------------------------------------ |
| `src/config`    | **Configuration**  | Loads environment variables (`.env`) via `settings.py`. |
| `src/database`  | **Infrastructure** | Manages connections to Postgres, Redis, and Mongo.      |
| `src/models`    | **Domain Layer**   | Python `dataclasses` representing core entities.        |
| `src/services`  | **Business Layer** | Contains logic for `OrderService`, `ProductService`.    |
| `src/pipelines` | **Data pipelines** | Scripts for Ingestion and Transformation.               |
| `src/analytics` | **Reporting**      | SQL repository for generating business reports.         |
