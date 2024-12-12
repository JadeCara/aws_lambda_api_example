import pytest
from pytest import param

from app.routes.users import is_existing_email_address, is_existing_user_id, is_existing_user_name

user_data_1 = {
    "Id": "1",
    "user_name": "johndoe",
    "password": "password",
    "email_address": "john@example.com",
}
user_data_2 = {
    "Id": "2",
    "user_name": "janedoe",  # Duplicate user_name
    "password": "password123",
    "email_address": "jane@example.com",
}

user_data_3 = {
    "Id": "3",
    "user_name": "jondoe",
    "password": "password",
    "email_address": "john@example.com",
}

user_not_found = {"detail": "User not found"}


def generate_users(client, users):
    for user in users:
        client.post("/users/", json=user)


def test_is_existing_user_id(client):
    assert is_existing_user_id("1") is False

    client.post("/users/", json=user_data_1)
    assert is_existing_user_id("1") is True


def test_is_existing_user_name(client):
    assert is_existing_user_name("johndoe") is False

    client.post("/users/", json=user_data_1)
    assert is_existing_user_name("johndoe") is True


def test_is_existing_email_address(client):
    assert is_existing_email_address("john@example.com") is False

    client.post("/users/", json=user_data_1)
    assert is_existing_email_address("john@example.com") is True


@pytest.mark.parametrize(
    "users",
    [
        param([], id="no_users_created"),
        param([user_data_1], id="one_user"),
        param([user_data_1, user_data_2], id="multiple_users"),
    ],
)
def test_read_users(client, users):
    # empty response
    response = client.get("/users/")
    assert response.status_code == 200
    assert response.json() == []

    generate_users(client, users)

    response = client.get("/users/")
    assert response.status_code == 200
    assert response.json() == users


@pytest.mark.parametrize(
    "user_Id, users, expected_status, expected_response",
    [
        param("1", [user_data_1], 200, user_data_1, id="user_found_only_user"),
        param("1", [user_data_1, user_data_2], 200, user_data_1, id="user1_found_multiple_users"),
        param("2", [user_data_1, user_data_2], 200, user_data_2, id="user2_found_multipl_users"),
        param("75", [], 404, user_not_found, id="user75_not_found_no_users"),
        param(
            "75",
            [user_data_1, user_data_2],
            404,
            user_not_found,
            id="user75_not_found_multiple_users",
        ),
    ],
)
def test_read_user(client, user_Id, users, expected_status, expected_response):
    generate_users(client, users)

    response = client.get(f"/users/{user_Id}")
    assert response.status_code == expected_status
    assert response.json() == expected_response


def test_create_user(client):
    response = client.post("/users/", json=user_data_1)
    assert response.status_code == 200
    assert response.json() == {"message": "User created"}
    assert user_data_1 in client.get("/users/").json()


def test_cannot_create_duplicate_user_name(client):
    client.post("/users/", json=user_data_1)
    response = client.post("/users/", json=user_data_1)
    assert response.status_code == 400
    assert response.json() == {"detail": "User name already exists"}


def test_cannot_create_duplicate_user_email(client):
    client.post("/users/", json=user_data_1)

    response = client.post("/users/", json=user_data_3)
    assert response.status_code == 400
    assert response.json() == {"detail": "Email address already exists"}


def test_update_user(client):
    # add user to db
    client.post("/users/", json=user_data_1)

    # update user
    response = client.put("/users/1", json=user_data_3)
    print(response.json())  # Print the response content for debugging
    assert response.status_code == 200
    assert response.json() == {
        "message": "User with id 1 updated",
        "updated_attributes": {"user_name": "jondoe"},
    }


def test_update_user_must_exist(client):
    response = client.put("/users/1", json=user_data_3)
    print(response.json())  # Print the response content for debugging
    assert response.status_code == 400
    assert response.json() == {"detail": "User Id not found."}


def test_delete_user(client):
    # add user to db
    client.post("/users/", json=user_data_1)

    response = client.delete("/users/1")
    assert response.status_code == 200
    assert response.json() == {"message": "User with id 1 deleted"}


def test_cannot_delete_user_that_does_not_exist(client):
    response = client.delete("/users/1")
    assert response.status_code == 400
    assert response.json() == {"detail": "User Id not found."}
