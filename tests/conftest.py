import pytest
from botocore.stub import Stubber
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client():
    with TestClient(app) as client:
        yield client


@pytest.fixture
def mock_dynamodb(request):
    table = request.param
    with Stubber(table.meta.client) as stubber:
        yield stubber
        stubber.assert_no_pending_responses()
