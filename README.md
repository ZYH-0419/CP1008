# CP1008 Group Project  
## Centralised Validation & Error Handling (FastAPI Demo)

---

## Project Overview

This project demonstrates a non-trivial architectural improvement in an existing Python codebase.

The selected feature is:

> **Centralised validation and standardised error handling**

The objective is to improve:

- Architectural integrity  
- Consistency of API responses  
- Test coverage (especially negative cases)  
- Documentation clarity  

This project supports the Think–Reflect–Improve framework by demonstrating how generative AI tools can assist in improving software design and development workflows.

---

## Application Description

The application is a simplified **Item Management API** built using FastAPI.

It provides the following endpoints:

- `GET /items/{item_id}` – Retrieve an item  
- `POST /items` – Create a new item  

The application uses in-memory storage for simplicity.

Example item:

```json
{
  "name": "apple",
  "price": 1.2
}
```

---

## Baseline Version

File: `baseline_app.py`

Characteristics:

- Manual validation inside endpoints  
- Duplicated validation logic  
- Inconsistent error formats  
- Mixed HTTP status codes  
- Different `detail` structures returned  

This demonstrates how scattered validation logic reduces maintainability and complicates testing.

---

## Improved Version

File: `improved_app.py`

Improvements implemented:

- Schema-based validation using **Pydantic**
- Global exception handler for validation errors
- Custom application error class (`AppError`)
- Standardised JSON error response format

All errors now follow this structure:

```json
{
  "error_code": "VALIDATION_ERROR",
  "message": "Fix the highlighted fields and try again.",
  "details": [
    {
      "field": "price",
      "reason": "Input should be greater than 0"
    }
  ]
}
```

### Benefits

- Consistent error structure
- Clear feedback to API users
- Easier automated testing
- Improved maintainability
- Cleaner architectural separation

---

## Environment Setup

### Create Virtual Environment

```bash
python3 -m venv venv
```

### Activate Virtual Environment

macOS / Linux:

```bash
source venv/bin/activate
```

Windows:

```bash
venv\Scripts\activate
```

### Install Dependencies

```bash
pip install fastapi uvicorn pytest
```

---

## Running the Application

### Run Baseline Version

```bash
python -m uvicorn baseline_app:app --reload
```

Open browser:

```
http://127.0.0.1:8000/docs
```

### Run Improved Version

```bash
python -m uvicorn improved_app:app --reload
```

---

## Running Tests

```bash
pytest -q
```

---




