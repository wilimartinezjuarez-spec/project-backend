def test_register_user(client):
    response = client.post("/auth/register", json={
        "email": "usuario1@test.com",
        "password": "clave123"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "usuario1@test.com"
    assert "id" in data
    assert "password" not in data


def test_register_duplicate_email(client):
    client.post("/auth/register", json={
        "email": "usuario2@test.com",
        "password": "clave123"
    })
    response = client.post("/auth/register", json={
        "email": "usuario2@test.com",
        "password": "otraclave"
    })
    assert response.status_code == 400


def test_login_success(client):
    client.post("/auth/register", json={
        "email": "usuario3@test.com",
        "password": "clave123"
    })
    response = client.post("/auth/login", data={
        "username": "usuario3@test.com",
        "password": "clave123"
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password(client):
    client.post("/auth/register", json={
        "email": "usuario4@test.com",
        "password": "clave123"
    })
    response = client.post("/auth/login", data={
        "username": "usuario4@test.com",
        "password": "claveincorrecta"
    })
    assert response.status_code == 401