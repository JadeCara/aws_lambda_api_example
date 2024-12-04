import pytest
from botocore.stub import Stubber

from app.routes.users import table


@pytest.fixture
def mock_dynamodb():
    with Stubber(table.meta.client) as stubber:
        yield stubber
        stubber.assert_no_pending_responses()


def test_read_users(client, mock_dynamodb):
    mock_dynamodb.add_response(
        "scan",
        expected_params={"TableName": "users"},
        service_response={
            "Items": [
                {
                    "Id": {"S": "1"},
                    "user_name": {"S": "johndoe"},
                    "password": {"S": "password"},
                    "email_address": {"S": "john@example.com"},
                }
            ]
        },
    )
    response = client.get("/users/")
    assert response.status_code == 200
    assert response.json() == [
        {
            "Id": "1",
            "user_name": "johndoe",
            "password": "password",
            "email_address": "john@example.com",
        }
    ]


def test_read_user(client, mock_dynamodb):
    mock_dynamodb.add_response(
        "get_item",
        expected_params={
            "TableName": "users",
            "Key": {"Id": "1"},
        },
        service_response={
            "Item": {
                "Id": {"S": "1"},
                "user_name": {"S": "johndoe"},
                "password": {"S": "password"},
                "email_address": {"S": "john@example.com"},
            }
        },
    )
    response = client.get("/users/1")
    assert response.status_code == 200
    assert response.json() == {
        "Id": "1",
        "user_name": "johndoe",
        "password": "password",
        "email_address": "john@example.com",
    }


def test_create_user(client, mock_dynamodb):
    user_data = {
        "Id": "2",
        "user_name": "janedoe",
        "password": "password",
        "email_address": "jane@example.com",
    }
    mock_dynamodb.add_response(
        "put_item", expected_params={"TableName": "users", "Item": user_data}, service_response={}
    )
    response = client.post("/users/", json=user_data)
    assert response.status_code == 200
    assert response.json() == {"message": "User created"}


def test_update_user(client, mock_dynamodb):
    user_data = {
        "Id": "1",
        "user_name": "janedoeupdated",
        "password": "newpassword",
        "email_address": "janeupdated@example.com",
    }
    mock_dynamodb.add_response(
        "update_item",
        expected_params={
            "TableName": "users",
            "Key": {"Id": "1"},
            "UpdateExpression": "set user_name=:u, password=:p, email_address=:e",
            "ExpressionAttributeValues": {
                ":u": "janedoeupdated",
                ":p": "newpassword",
                ":e": "janeupdated@example.com",
            },
            "ReturnValues": "UPDATED_NEW",
        },
        service_response={"Attributes": {k: {"S": v} for k, v in user_data.items()}},
    )
    response = client.put("/users/1", json=user_data)
    print(response.json())  # Print the response content for debugging
    assert response.status_code == 200
    assert response.json() == {"message": "User with id 1 updated", "updated_attributes": user_data}


def test_delete_user(client, mock_dynamodb):
    mock_dynamodb.add_response(
        "delete_item",
        expected_params={"TableName": "users", "Key": {"Id": "1"}},
        service_response={},
    )
    response = client.delete("/users/1")
    assert response.status_code == 200
    assert response.json() == {"message": "User with id 1 deleted"}
