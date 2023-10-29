"""
Testing api endpoints
"""


from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


def test_hello_world():
    """
    Unit test for the hello world api
    """

    response = client.get("api/v1/hello")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}
