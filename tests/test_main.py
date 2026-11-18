
from fastapi.testclient import TestClient
import pytest

from app.api import app


@pytest.fixture
def expense_id(client):
    response = client.post(
        "/expenses",
        json={
            "title": "lunch",
            "amount": "150.00",
            "category": "food"
        }
    )

    assert response.status_code == 201
    return response.json()["id"]


def test_home(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "message": "Expense Tracker API is running"
    }


def test_add_expense(client):
    response = client.post(
        "/expenses",
        json={
            "title": "dinner",
            "amount": "200.00",
            "category": "food"
        }
    )

    assert response.status_code == 201

    data = response.json()

    assert data["title"] == "dinner"
    assert data["amount"] == "200.00"
    assert data["category"] == "food"
    assert "id" in data

def test_update_expense(client, expense_id):
    response = client.put(
        f"/update-expense/{expense_id}",
        json={
            "title": "updated lunch",
            "amount": "250.00",
            "category": "food"
        }
    )

    assert response.status_code == 200


def test_delete_expense(client, expense_id):
    response = client.delete(
        f"/delete-expense/{expense_id}"
    )

    assert response.status_code == 200

def test_invalid_expense(client):
    response = client.post(
        "/expenses",
        json={
            "title": "invalid",
            "amount": "-100",
            "category": "food"
        }
    )

    assert response.status_code == 422
