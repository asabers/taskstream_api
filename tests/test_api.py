"""
API Integration Tests
---------------------
Core testing suite for validating the TaskStream API endpoints 
using the FastAPI TestClient.
"""

def test_create_user(client):
    """Verifies that the registration endpoint accepts valid payloads 
    and returns the expected user structure.
    """
    response = client.post(
        "/users/",
        json={"email": "test@example.com", "password": "password123"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
    assert "id" in data

def test_create_task(client):
    """Validates the end-to-end task creation workflow, including
    initial user dependency setup.
    """
    # Initialize a user to satisfy foreign key requirements
    client.post("/users/", json={"email": "owner@example.com", "password": "password"})
    
    response = client.post(
        "/tasks/",
        json={"title": "Test Task", "description": "Verify the testing suite"}
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Test Task"

def test_health_check(client):
    """Standard check for service availability and metadata consistency."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "online", "version": "1.0.2-legacy"}

def test_update_status_simple(client):
    """Functional test for the task status update lifecycle."""
    # Ensure a task exists in the system
    client.post("/tasks/", json={"title": "Status Task"})
    # Execute status modification on the target record 
    response = client.put("/tasks/1/status")
    assert response.status_code == 200
    assert response.json()["status"] == "COMPLETED"