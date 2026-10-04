from fastapi.testclient import TestClient
from sqlagent.main import app

client = TestClient(app)


def test_runs_and_refuses_a_write():
    payload = client.post("/agent/run", json={"goal": 'revenue by region', **{'payload': {'rows': [{'region': 'north', 'revenue': 10}, {'region': 'south', 'revenue': 30}]}}}).json()
    assert payload["refused"] is False
    assert payload["applied"] is False
    assert payload["totals"]["south"] == 30
    refused = client.post("/agent/run", json={"goal": 'delete old rows'}).json()
    assert refused["refused"] is True
