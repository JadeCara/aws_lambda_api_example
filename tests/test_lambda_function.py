import pytest
from unittest.mock import patch, MagicMock
from lambda_function import lambda_handler


@pytest.mark.parametrize(
    "method, path, expected_status_code, expected_body",
    [
        ("GET", "/", 200, {"message": "Welcome to the API"}),
        ("GET", "/health", 200, {"message": "API is healthy"}),
        ("GET", "/users/", 200, {"message": "List of users"}),
        ("GET", "/users/1", 200, {"message": "User with id 1"}),
        ("POST", "/users/", 200, {"message": "User created"}),
        ("PUT", "/users/1", 200, {"message": "User with id 1 updated"}),
        ("DELETE", "/users/1", 200, {"message": "User with id 1 deleted"}),
        ("GET", "/posts/", 200, {"message": "List of posts"}),
        ("GET", "/posts/1", 200, {"message": "Post with id 1"}),
        ("POST", "/posts/", 200, {"message": "Post created"}),
        ("PUT", "/posts/1", 200, {"message": "Post with id 1 updated"}),
        ("DELETE", "/posts/1", 200, {"message": "Post with id 1 deleted"}),
    ],
)
def test_mangum_handler(client, method, path, expected_status_code, expected_body):
    event = {
        "httpMethod": method,
        "path": path,
        "headers": {"Accept": "application/json", "Content-Type": "application/json"},
        "multiValueHeaders": {"Accept": ["application/json"], "Content-Type": ["application/json"]},
        "queryStringParameters": None,
        "multiValueQueryStringParameters": None,
        "pathParameters": None,
        "stageVariables": None,
        "requestContext": {
            "resourceId": "123456",
            "resourcePath": path,
            "httpMethod": method,
            "extendedRequestId": "abcdefg12345",
            "requestTime": "10/Oct/2020:12:34:56 +0000",
            "path": path,
            "accountId": "123456789012",
            "protocol": "HTTP/1.1",
            "stage": "dev",
            "domainPrefix": "example",
            "requestTimeEpoch": 1602339296000,
            "requestId": "abcdefg-1234-5678-90ab-cdefghijklmn",
            "identity": {"sourceIp": "192.168.0.1", "userAgent": "PostmanRuntime/7.26.8"},
            "domainName": "example.execute-api.us-east-1.amazonaws.com",
            "apiId": "abcdefg123",
        },
        "body": None,
        "isBase64Encoded": False,
    }
    with patch("lambda_function.handler") as m_handler:
        mock_handler = MagicMock()
        m_handler.return_value = mock_handler
        lambda_handler(event, None)
        m_handler.assert_called_once_with(event, None)
