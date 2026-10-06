import pytest
from fastapi.testclient import TestClient
from sqlagent.main import app

client = TestClient(app)


def test_decimal_totals_preserve_accounting_result():
    r = client.post("/agent/run", json={"goal": "total revenue", "payload": {"rows": [{"region": "north", "revenue": "0.1"}, {"region": "north", "revenue": "0.2"}]}}).json()
    assert r["totals"]["north"] == 0.3
    assert r["totals_decimal"]["north"] == "0.3"
    assert r["region_counts"] == {"north": 2}


@pytest.mark.parametrize("rows", [[42], [{"revenue": "NaN"}], [{"revenue": "Infinity"}], [{"revenue": "1e1000000"}], [{"revenue": True}], [{"revenue": "0.0000001"}], [{"region": None}], {"bad": 1}])
def test_invalid_rows_return_422_instead_of_server_error(rows):
    assert client.post("/agent/run", json={"goal": "aggregate", "payload": {"rows": rows}}).status_code == 422


def test_non_mapping_payload_is_rejected():
    assert client.post("/agent/run", json={"goal": "aggregate", "payload": [1]}).status_code == 422
