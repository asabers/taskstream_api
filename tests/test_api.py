def test_create_user(client):
    response = client.post(
        "/users/",
        json={"email": "test@example.com", "password": "password123"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
    assert "id" in data

def test_create_task(client):
    # First create a user to ensure the DB isn't empty
    client.post("/users/", json={"email": "owner@example.com", "password": "password"})
    
    response = client.post(
        "/tasks/",
        json={"title": "Test Task", "description": "Verify the testing suite"}
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Test Task"

def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "online", "version": "1.0.2-legacy"}

def test_update_status_simple(client):
    # Setup: Create a user and a task
    client.post("/users/", json={"email": "owner@example.com", "password": "password"})
    client.post("/tasks/", json={"title": "Status Task"})
    
    # Test: Update status
    response = client.put("/tasks/1/status")
    
    # --- ADD THESE PRINT STATEMENTS ---
    print("\n--- API RAW RESPONSE ---")
    print(response.json())
    print("------------------------\n")
    
    assert response.status_code == 200
    # Use .get() to prevent a KeyError from crashing the test immediately
    assert response.json().get("status") == "COMPLETED"