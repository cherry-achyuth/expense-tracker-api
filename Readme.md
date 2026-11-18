# Expense Tracker REST API

A RESTful API for managing personal expenses, built with **Python, FastAPI, PostgreSQL and SQLAlchemy**.

This project demonstrates backend development fundamentals, database integration, request validation, pagination, SQL aggregation and automated API testing.

## Features

- Create expenses with input validation.
- Retrieve expenses with category filtering.
- Update and delete expenses.
- Paginate expense records.
- Generate total expense and category-wise summaries.
- Store financial amounts using Decimal.
- Handle database errors with transaction rollback and logging.
- Validate API responses using Pydantic schemas.
- Automated API tests using Pytest and FastAPI TestClient.
- Separate PostgreSQL database for testing.

## Technology Stack

| Technology   | Purpose                     |
| ------------ | --------------------------- |
| Python       | Programming language        |
| FastAPI      | REST API framework          |
| PostgreSQL   | Relational database         |
| SQLAlchemy   | ORM and database operations |
| Pydantic     | Data validation and schemas |
| Pytest       | Automated testing           |
| Git & GitHub | Version control             |

## Project Structure

```text
expense-tracker-api/
│
├── app/
│   ├── __init__.py
│   ├── api.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   └── create_tables.py
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   └── test_main.py
│
├── .env
├── .gitignore
├── requirements.txt
├── requirements-dev.txt
└── README.md
```

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/cherry-achyuth/expense-tracker-api.git

cd expense-tracker-api
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```powershell
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements-dev.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
DATABASE_URL=postgresql+psycopg://postgres:YOUR_PASSWORD@localhost:5432/expense_tracker

TEST_DATABASE_URL=postgresql+psycopg://postgres:YOUR_PASSWORD@localhost:5432/expense_tracker_test
```

Replace the password with your PostgreSQL password.

Create both PostgreSQL databases before running the application or tests.

### 5. Create database tables

```bash
python -m app.create_tables
```

### 6. Start the API

```bash
uvicorn app.api:app --reload
```

The API will be available at:

`http://127.0.0.1:8000`

Interactive API documentation:

`http://127.0.0.1:8000/docs`

## API Endpoints

| Method | Endpoint                       | Description        |
| ------ | ------------------------------ | ------------------ |
| GET    | `/`                            | API health message |
| POST   | `/expenses`                    | Create an expense  |
| GET    | `/expenses`                    | List expenses      |
| GET    | `/expenses?category=Food`      | Filter by category |
| GET    | `/expenses?skip=0&limit=10`    | Paginated expenses |
| GET    | `/expenses/summary`            | Expense summary    |
| PUT    | `/update-expense/{expense_id}` | Update an expense  |
| DELETE | `/delete-expense/{expense_id}` | Delete an expense  |

## Example Request

### Create an expense

`POST /expenses`

```json
{
  "title": "Lunch",
  "amount": "250.00",
  "category": "Food"
}
```

### Expense summary

`GET /expenses/summary`

Returns the total number of expenses, total spending and category-wise spending.

## Running Tests

Make sure your test database is configured in `.env`.

Run:

```bash
python -m pytest -v
```

The tests use a separate PostgreSQL database and transaction rollback to isolate test data.

## Future Improvements

- Authentication and user-specific expenses.
- Date-based filtering.
- Database migrations with Alembic.
- Docker and Docker Compose.
- Cloud deployment.
- CI/CD integration.

## Author

**Charan Teja**

GitHub: [https://github.com/cherry-achyuth](https://github.com/cherry-achyuth)
