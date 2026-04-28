from pathlib import Path
import sys

import pytest
from fastapi.testclient import TestClient

# Make this file work both with `pytest` and with
# `python3 tests/test_tasks_api.py` from the project root.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from app import routes
from app.main import app


client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_in_memory_storage() -> None:
    """Start every test with an empty task list.

    The API stores tasks in normal Python variables, so tests need to clear
    those variables to avoid leaking data from one test into the next.
    """

    routes.tasks.clear()
    routes.next_task_id = 1


def test_health_check_returns_ok() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_list_tasks_starts_empty() -> None:
    response = client.get("/tasks")

    assert response.status_code == 200
    assert response.json() == []


def test_create_task() -> None:
    response = client.post(
        "/tasks",
        json={"title": "Learn FastAPI", "completed": False},
    )

    assert response.status_code == 201
    assert response.json() == {
        "id": 1,
        "title": "Learn FastAPI",
        "completed": False,
    }


def test_create_task_defaults_completed_to_false() -> None:
    response = client.post("/tasks", json={"title": "Write tests"})

    assert response.status_code == 201
    assert response.json()["completed"] is False


def test_create_task_requires_title() -> None:
    response = client.post("/tasks", json={"completed": False})

    assert response.status_code == 422


def test_create_task_rejects_empty_title() -> None:
    response = client.post("/tasks", json={"title": ""})

    assert response.status_code == 422


def test_create_task_rejects_unknown_fields() -> None:
    response = client.post(
        "/tasks",
        json={"title": "Learn FastAPI", "priority": "high"},
    )

    assert response.status_code == 422


def test_list_tasks_returns_created_tasks() -> None:
    client.post("/tasks", json={"title": "First task"})
    client.post("/tasks", json={"title": "Second task", "completed": True})

    response = client.get("/tasks")

    assert response.status_code == 200
    assert response.json() == [
        {"id": 1, "title": "First task", "completed": False},
        {"id": 2, "title": "Second task", "completed": True},
    ]


def test_update_task() -> None:
    create_response = client.post("/tasks", json={"title": "Old title"})
    task_id = create_response.json()["id"]

    response = client.put(
        f"/tasks/{task_id}",
        json={"title": "New title", "completed": True},
    )

    assert response.status_code == 200
    assert response.json() == {
        "id": task_id,
        "title": "New title",
        "completed": True,
    }


def test_update_task_replaces_the_whole_task() -> None:
    create_response = client.post(
        "/tasks",
        json={"title": "Old title", "completed": True},
    )
    task_id = create_response.json()["id"]

    response = client.put(f"/tasks/{task_id}", json={"title": "New title"})

    assert response.status_code == 200
    assert response.json() == {
        "id": task_id,
        "title": "New title",
        "completed": False,
    }


def test_update_missing_task_returns_404() -> None:
    response = client.put("/tasks/999", json={"title": "No task"})

    assert response.status_code == 404
    assert response.json() == {"detail": "Task not found"}


def test_update_task_rejects_invalid_completed_value() -> None:
    client.post("/tasks", json={"title": "Existing task"})

    response = client.put("/tasks/1", json={"completed": "not a boolean"})

    assert response.status_code == 422


def test_delete_task() -> None:
    create_response = client.post("/tasks", json={"title": "Delete me"})
    task_id = create_response.json()["id"]

    delete_response = client.delete(f"/tasks/{task_id}")
    list_response = client.get("/tasks")

    assert delete_response.status_code == 204
    assert delete_response.content == b""
    assert list_response.json() == []


def test_delete_missing_task_returns_404() -> None:
    response = client.delete("/tasks/999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Task not found"}


def test_task_id_must_be_an_integer() -> None:
    response = client.delete("/tasks/not-an-integer")

    assert response.status_code == 422


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__]))
