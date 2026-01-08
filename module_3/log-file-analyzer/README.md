# Log File Analyzer (Lab 2)

## Overview

This tool identifies patterns in a web server log file using Regular Expressions and processes the data using functional programming concepts like generators and iterators. It parses log entries to extract meaningful insights such as status code counts, total data transfer size, and top active IP addresses.

## Project Structure

```
module_3/log-file-analyzer/
├── log_file_analyzer/      # Main package
│   ├── models/             # Data models (LogEntry)
│   ├── services/           # Business logic (IO, Parsing, Analysis, Reporting)
│   ├── utils/              # Utility functions
│   ├── config.py           # Configuration settings
│   └── main.py             # Entry point
├── tests/                  # Test suite
├── pyproject.toml          # Poetry configuration
└── sample.log              # Sample log file for testing
```

## Setup Instructions

1.  **Navigate to the lab directory:**

    ```bash
    cd module_3/log-file-analyzer
    ```

2.  **Install dependencies using Poetry:**

    ```bash
    poetry install
    ```

3.  **Activate the virtual environment:**

    ```bash
    poetry shell
    ```

## Usage

Run the analyzer on the default sample log file:

```bash
python -m log_file_analyzer.main
```

Or specify a custom log file path:

```bash
python -m log_file_analyzer.main path/to/your.log
```

## Testing

Run the test suite:

```bash
pytest
```
