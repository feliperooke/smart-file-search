# Smart File Search (Backend)

This is the backend of the Smart File Search project, built with FastAPI and managed using Poetry.

## Requirements
- Python 3.11

---

## 🚀 Getting Started

### 1. Install Poetry
Follow instructions: https://python-poetry.org/docs/#installation

Or use:
```bash
curl -sSL https://install.python-poetry.org | python3 -
```
### 2. Setup the project
```bash
cd backend
poetry env activate
```

### 3. Run the development server
```bash
poetry shell
poetry run uvicorn app.main:app --reload
```