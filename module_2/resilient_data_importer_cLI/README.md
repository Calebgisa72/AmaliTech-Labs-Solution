# Lab 1: Resilient Data Importer CLI

## Introduction

This lab implements a robust Command Line Interface (CLI) tool designed to import user data from CSV files into a persistent JSON-based storage system. It focuses on resilience, error handling, and data integrity, ensuring that malformed data or duplicates do not crash the application or corrupt the database.

## Architecture

The application is structured into modular components, each with a specific responsibility:

### Components

1.  **CLI (`resilient_importer/cli.py`)**:

    - The entry point of the application.
    - Handles command-line argument parsing (`csvfile`, `--db`).
    - Initializes the `UserRepository` and `Importer` services.
    - Displays the final summary of the import process (successes, duplicates, errors).

2.  **Parser (`resilient_importer/parser.py`)**:

    - Responsibilities: Reads the input CSV file.
    - Validates the file format and required headers (`user_id`, `name`, `email`).
    - Yields valid `User` objects or raises detailed errors for malformed rows.

3.  **Importer (`resilient_importer/importer.py`)**:

    - The core logic engine.
    - Orchestrates the flow between the Parser and Storage.
    - Performs business logic checks, such as detecting duplicate users by ID or Email.
    - Aggregates results (counts and error logs) for the CLI summary.

4.  **Storage (`resilient_importer/storage.py`)**:

    - Manages data persistence.
    - Implements `UserRepository` to abstract file I/O.
    - Reads from and writes to a JSON file (`data/users.json` by default).
    - Ensures atomic-like saves and handles file system errors.

5.  **Models (`resilient_importer/models/user_model.py`)**:
    - Defines the `User` data structure using Python dataclasses for type safety.

### Execution Flow

1.  **Start**: User runs the CLI with a target CSV.
2.  **Parse**: `Parser` reads the CSV row by row.
3.  **Process**: For each row, `Importer` checks if the user already exists in `Storage`.
4.  **Persist**: If new and valid, `Storage` saves the user to the JSON database.
5.  **Report**: The CLI outputs a summary of the operation.

## Setup & Installation

### Prerequisites

- Python 3.8 or higher
- Git
- [Poetry](https://python-poetry.org/) (Recommended for dependency management)

### Installation Steps

1.  **Clone the Repository**
    Clone the full monorepo to your local machine:

    ```bash
    git clone https://github.com/Calebgisa72/AmaliTech-Labs-Solution.git
    ```

2.  **Navigate to the Lab Directory**
    Move into the specific directory for Lab 1:

    ```bash
    cd "AmaliTech-Labs-Solution/module_2/Resilient Data Importer CLI"
    ```

3.  **Create and Activate a Virtual Environment**
    It is best practice to run Python projects in an isolated environment.

    **On Windows:**

    ```powershell
    python -m venv venv
    venv\Scripts\activate
    ```

4.  **Install Dependencies**
    Use the recommended package manager (Poetry) to install dependencies:
    ```bash
    poetry install
    ```
    _This will read `pyproject.toml` and install all necessary packages into the virtual environment._

## Usage

Ensure your virtual environment is active before running commands.

### Basic Command

Import users from a CSV file:

```bash
poetry run python -m resilient_importer.cli data/users.csv
```

_(Make sure to replace `data/users.csv` with the actual path to your CSV file)_

### Options

- `--db <path>`: Specify a custom path for the JSON database file.
  ```bash
  poetry run python -m resilient_importer.cli data/users.csv --db my_database.json
  ```

## Testing

The project includes a test suite to verify functionality. Run tests using `pytest`:

```bash
poetry run pytest
```
