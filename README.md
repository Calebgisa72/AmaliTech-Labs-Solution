# AmaliTech Labs Solution

This repository serves as a centralized monorepo containing solutions for the AmaliTech Apprenticeship program. It demonstrates progressive learning across various domains, ranging from fundamental Object-Oriented Programming (OOP) to advanced topics like Test-Driven Development (TDD), Clean Architecture, and Robust CLI handling.

## 📂 Lab Overview

The following table provides a high-level summary of the labs completed in this repository, detailing their purpose, key technical concepts, and execution commands.

| Module       | Lab Name                                                                       | Purpose                                                                                       | Key Concepts                                                        | Run Command (inside lab dir)                                 |
| :----------- | :----------------------------------------------------------------------------- | :-------------------------------------------------------------------------------------------- | :------------------------------------------------------------------ | :----------------------------------------------------------- |
| **Module 1** | **[Employee Payroll Tracker](module_1/Employee%20Payroll%20Tracker%20System)** | Command-line system to manage employee types and generate payslips.                           | Inheritance, Polymorphism, Abstraction, Encapsulation               | `python main.py`                                             |
| **Module 1** | **[Library Inventory App](module_1/Library%20Inventory%20Application)**        | Manages library assets (books, audiobooks), authors, and loans with overdue logic.            | Abstract Base Classes, Composition, Date manipulation               | `python main.py`                                             |
| **Module 1** | **[Student Course System](module_1/Student%20Course%20Management%20System)**   | Administers student enrollments, courses, and grading.                                        | Composition, Data Dictionary Storage, Modular Design                | `python main.py`                                             |
| **Module 2** | **[Resilient Data Importer](module_2/Resilient%20Data%20Importer%20CLI)**      | Robust CLI tool for importing/deduplication of CSV user data into JSON storage.               | File I/O, Exception Handling, Generators, Dataclasses               | `poetry run python -m resilient_importer.cli data/users.csv` |
| **Module 2** | **[TDD Weather API Stub](module_2/ttd-based-weather-api)**                     | A weather service stub designed to demonstrate high-quality software engineering practices.   | TDD (Test-Driven Development), SOLID Principles, Clean Architecture | `pytest`                                                     |
| **Module 3** | **[Student Grade Analytics](module_3/student_grade_analytics_tool)**           | CLI tool for analyzing student grades using advanced collections and generating JSON reports. | Advanced Collections, Dataclasses, IO Context Managers              | `python -m student_analytics.main`                           |

## 🚀 Getting Started

### Prerequisites

- **Python 3.8+** (Required for all labs)
- **Poetry** (Recommended for Module 2 labs)

### Installation

Clone the entire repository to access all labs:

```bash
git clone https://github.com/Calebgisa72/AmaliTech-Labs-Solution.git
cd AmaliTech-Labs-Solution
```

### Running a Specific Lab

Navigate to the directory of the specific lab you wish to run and follow the "Run Command" listed in the table above.
For **Module 2** labs, ensure you install dependencies first:

```bash
# Example for Module 2
cd "module_2/Resilient Data Importer CLI"
poetry install
poetry shell
```

## 🛠️ Technologies

- **Language**: Python 3
- **Testing**: pytest
- **Management**: Poetry
- **Version Control**: Git
