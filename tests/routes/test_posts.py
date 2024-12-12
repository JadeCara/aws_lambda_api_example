import pytest

from app.routes.posts import table


@pytest.mark.parametrize("mock_dynamodb", [table], indirect=True)
def test_read_posts(client, mock_dynamodb):
    mock_dynamodb.add_response(
        "scan",
        expected_params={"TableName": "posts"},
        service_response={
            "Items": [
                {
                    "Id": {"S": "1"},
                    "title": {"S": "First Post"},
                    "content": {"S": "This is the first post"},
                    "author_id": {"S": "1"},
                }
            ]
        },
    )
    response = client.get("/posts/")
    print(response.json())  # Print the response content for debugging
    assert response.status_code == 200
    assert response.json() == [
        {"Id": "1", "title": "First Post", "content": "This is the first post", "author_id": "1"}
    ]


@pytest.mark.parametrize("mock_dynamodb", [table], indirect=True)
def test_read_post(client, mock_dynamodb):
    mock_dynamodb.add_response(
        "get_item",
        expected_params={"TableName": "posts", "Key": {"Id": "1"}},
        service_response={
            "Item": {
                "Id": {"S": "1"},
                "title": {"S": "First Post"},
                "content": {"S": "This is the first post"},
                "author_id": {"S": "1"},
            }
        },
    )
    response = client.get("/posts/1")
    print(response.json())  # Print the response content for debugging
    assert response.status_code == 200
    assert response.json() == {
        "Id": "1",
        "title": "First Post",
        "content": "This is the first post",
        "author_id": "1",
    }


@pytest.mark.parametrize("mock_dynamodb", [table], indirect=True)
def test_create_post(client, mock_dynamodb):
    post_data = {
        "Id": "2",
        "title": "Second Post",
        "content": "This is the second post",
        "author_id": "2",
    }
    mock_dynamodb.add_response(
        "put_item", expected_params={"TableName": "posts", "Item": post_data}, service_response={}
    )
    response = client.post("/posts/", json=post_data)
    print(response.json())  # Print the response content for debugging
    assert response.status_code == 200
    assert response.json() == {"message": "Post created"}


@pytest.mark.parametrize("mock_dynamodb", [table], indirect=True)
def test_update_post(client, mock_dynamodb):
    post_data = {
        "Id": "1",
        "title": "Updated Post",
        "content": "This is the updated post",
        "author_id": "2",
    }
    mock_dynamodb.add_response(
        "update_item",
        expected_params={
            "TableName": "posts",
            "Key": {"Id": "1"},
            "UpdateExpression": "set title=:t, content=:c, author_id=:a",
            "ExpressionAttributeValues": {
                ":t": "Updated Post",
                ":c": "This is the updated post",
                ":a": "2",
            },
            "ReturnValues": "UPDATED_NEW",
        },
        service_response={
            "Attributes": {
                "Id": {"S": "1"},
                "title": {"S": "Updated Post"},
                "content": {"S": "This is the updated post"},
                "author_id": {"S": "2"},
            }
        },
    )
    response = client.put("/posts/1", json=post_data)
    assert response.status_code == 200
    assert response.json() == {"message": "Post with id 1 updated", "updated_attributes": post_data}


@pytest.mark.parametrize("mock_dynamodb", [table], indirect=True)
def test_delete_post(client, mock_dynamodb):
    mock_dynamodb.add_response(
        "delete_item",
        expected_params={"TableName": "posts", "Key": {"Id": "1"}},
        service_response={},
    )
    response = client.delete("/posts/1")
    print(response.json())  # Print the response content for debugging
    assert response.status_code == 200
    assert response.json() == {"message": "Post with id 1 deleted"}
