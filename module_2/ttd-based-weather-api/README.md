# 🌦️ Lab 2 – TDD-based Weather API Service Stub

This project is **Lab 2** of the AmaliTech Software Engineering track.  
It demonstrates **Test-Driven Development (TDD)**, **clean architecture**, and **SOLID principles** by implementing a **Weather API service stub**.

The service is intentionally designed as a **stub** (no real external API calls) to focus on:
- Design correctness
- Test quality
- Architecture clarity
- Engineering discipline

---

## 📌 Project Goals

| Goal | Description |
|----|----|
| TDD | Tests are written **before** implementation |
| SOLID | Clean separation of concerns |
| Extensibility | Easy to add real API providers later |
| Testability | Fully testable without network access |
| Maintainability | Clear structure and documentation |

---

## 🧱 Project Structure

```text
lab_2_weather_service/
│
├── weather_service/        # Application code
│   ├── models.py
│   ├── exceptions.py
│   ├── providers.py
│   ├── service.py
│   └── logging_conf.py
│
├── tests/                  # Test suite (TDD)
│   ├── conftest.py
│   ├── test_service_success.py
│   ├── test_service_errors.py
│   ├── test_providers.py
│   └── test_logging.py
│
├── docs/
│   └── architecture.md
│
├── pyproject.toml
├── README.md
└── .pre-commit-config.yaml
