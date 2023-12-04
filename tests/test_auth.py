def test_register_user(client):
    valid_user_data = {
        "password": "testpassword",
        "email": "testuser@example.com",
        "first_name": "khushal",
        "last_name": "chouhan",
    }
    response = client.post("/register", json=valid_user_data)
    assert response.status_code == 201
    assert "id" in response.json


def test_register_user_invalid_data(client):
    invalid_user_data = {
        "email": "testuser@example.com",
        "password": "testpassword"
        # missing username
    }
    response = client.post("/register", json=invalid_user_data)
    assert response.status_code == 400


def test_login_user(client, fake_user_data):
    valid_credentials = {
        "username": fake_user_data.get("email"),
        "password": fake_user_data.get("password"),
    }
    response = client.post("/login", data=valid_credentials)
    assert response.status_code == 200
    assert "access_token" in response.json


def test_login_user_invalid_credentials(client):
    invalid_credentials = {
        "username": "testuser@example.com",
        "password": "wrongpassword",
    }
    response = client.post("/login", data=invalid_credentials)
    assert response.status_code == 400
