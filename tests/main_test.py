"""_summary_
"""

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_hello_world():
    """test fpr the hello world api"""

    response = client.get("api/v1/hello-world")

    assert response.status_code == 200
    assert response.json() == {"message": "hello from v1"}
