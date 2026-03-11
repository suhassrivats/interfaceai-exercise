"""API tests using TestClient. Requires Postgres (e.g. CI service or local)."""
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    """Health endpoint returns 200."""
    r = client.get("/api/health")
    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "ok"
    assert "timestamp" in data


def test_list_todos_empty():
    """Initially todos list is empty or returns 200."""
    r = client.get("/api/todos")
    assert r.status_code == 200
    assert isinstance(r.json(), list)


def test_create_and_list_todo():
    """Create a todo and then list it."""
    r = client.post(
        "/api/todos",
        json={"title": "Test todo", "description": "From test", "completed": False},
    )
    assert r.status_code == 201
    data = r.json()
    assert data["title"] == "Test todo"
    assert data["description"] == "From test"
    assert data["completed"] is False
    assert "id" in data
    todo_id = data["id"]

    r2 = client.get("/api/todos")
    assert r2.status_code == 200
    items = r2.json()
    assert any(t["id"] == todo_id for t in items)

    r3 = client.get(f"/api/todos/{todo_id}")
    assert r3.status_code == 200
    assert r3.json()["title"] == "Test todo"


def test_update_todo():
    """Update a todo."""
    r = client.post("/api/todos", json={"title": "Update me", "completed": False})
    assert r.status_code == 201
    todo_id = r.json()["id"]

    r2 = client.patch(f"/api/todos/{todo_id}", json={"completed": True})
    assert r2.status_code == 200
    assert r2.json()["completed"] is True


def test_delete_todo():
    """Delete a todo."""
    r = client.post("/api/todos", json={"title": "Delete me"})
    assert r.status_code == 201
    todo_id = r.json()["id"]

    r2 = client.delete(f"/api/todos/{todo_id}")
    assert r2.status_code == 204

    r3 = client.get(f"/api/todos/{todo_id}")
    assert r3.status_code == 404


def test_get_nonexistent_returns_404():
    """Get non-existent todo returns 404."""
    r = client.get("/api/todos/99999")
    assert r.status_code == 404
