# Student Grade Analytics Tool (Lab 1)

## Overview

This tool processes student records from CSV files, calculates advanced statistics (averages, rankings, distributions), and generates structured JSON reports. It utilizes Python's advanced collections (`Counter`, `defaultdict`, `OrderedDict`, `deque`) for efficient data processing.

## Project Structure

```
module_3/
├── student_analytics/      # Main package
│   ├── models/             # Data models (Student, Course, Grade)
│   ├── services/           # Business logic (IO, Analysis)
│   └── main.py             # Entry point
├── tests/                  # Test suite
├── ARCHITECTURE.md         # System design documentation
├── pyproject.toml          # Poetry configuration
└── requirements.txt        # Minimal requirements
```

## Setup Instructions

1. **Navigate to the lab directory:**

   ```bash
   cd module_3
   ```

2. **Create and activate a virtual environment:**

   ```bash
   python -m venv venv
   # Windows
   .\venv\Scripts\activate
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies using Poetry:**
   ```bash
   pip install poetry
   poetry config virtualenvs.create false --local
   poetry install
   ```

## Usage

python -m student_analytics.main data/sample_students.csv

## Testing

Run the test suite:

```bash
pytest
```

Run type checking:

```bash
mypy .
```
