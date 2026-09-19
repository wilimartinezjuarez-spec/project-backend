def get_auth_token(client, email="tareas@test.com", password="clave123"):
    client.post("/auth/register", json={"email": email, "password": password})
    response = client.post("/auth/login", data={"username": email, "password": password})
    return response.json()["access_token"]


def test_create_task_requires_auth(client):
    response = client.post("/tasks/", json={"title": "Sin token"})
    assert response.status_code == 401


def test_create_task_success(client):
    token = get_auth_token(client)
    headers = {"Authorization": f"Bearer {token}"}

    response = client.post("/tasks/", json={
        "title": "Comprar pan",
        "description": "Ir a la panadería",
        "completed": False
    }, headers=headers)

    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Comprar pan"
    assert "id" in data
    assert "user_id" in data


def test_get_tasks_only_own(client):
    token_a = get_auth_token(client, "usuarioA@test.com", "clave123")
    token_b = get_auth_token(client, "usuarioB@test.com", "clave123")

    client.post("/tasks/", json={"title": "Tarea de A"},
                 headers={"Authorization": f"Bearer {token_a}"})
    client.post("/tasks/", json={"title": "Tarea de B"},
                 headers={"Authorization": f"Bearer {token_b}"})

    response_a = client.get("/tasks/", headers={"Authorization": f"Bearer {token_a}"})
    tareas_a = response_a.json()

    assert len(tareas_a) == 1
    assert tareas_a[0]["title"] == "Tarea de A"


def test_get_task_not_found(client):
    token = get_auth_token(client)
    headers = {"Authorization": f"Bearer {token}"}

    response = client.get("/tasks/9999", headers=headers)
    assert response.status_code == 404


def test_update_task(client):
    token = get_auth_token(client)
    headers = {"Authorization": f"Bearer {token}"}

    create_response = client.post("/tasks/", json={"title": "Original"}, headers=headers)
    task_id = create_response.json()["id"]

    update_response = client.put(f"/tasks/{task_id}", json={"completed": True}, headers=headers)

    assert update_response.status_code == 200
    assert update_response.json()["completed"] is True


def test_delete_task(client):
    token = get_auth_token(client)
    headers = {"Authorization": f"Bearer {token}"}

    create_response = client.post("/tasks/", json={"title": "Para borrar"}, headers=headers)
    task_id = create_response.json()["id"]

    delete_response = client.delete(f"/tasks/{task_id}", headers=headers)
    assert delete_response.status_code == 200

    get_response = client.get(f"/tasks/{task_id}", headers=headers)
    assert get_response.status_code == 404