import pytest
from fastapi.testclient import TestClient
from moto import mock_aws
import boto3

from app.main import app


@pytest.fixture
def client(ddb_client):
    dynamodb = get_dynamodb(ddb_client)  # noqa F841
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="function")
def ddb_client():
    with mock_aws():
        yield boto3.client("dynamodb")


def get_dynamodb(ddb_client):
    tables = ["users", "posts"]
    for table_name in tables:
        ddb_client.create_table(
            TableName=table_name,
            KeySchema=[{"AttributeName": "Id", "KeyType": "HASH"}],
            AttributeDefinitions=[{"AttributeName": "Id", "AttributeType": "S"}],
            ProvisionedThroughput={"ReadCapacityUnits": 5, "WriteCapacityUnits": 5},
        )
