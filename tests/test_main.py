def test_read_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the API"}


def test_read_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"message": "API is healthy"}
