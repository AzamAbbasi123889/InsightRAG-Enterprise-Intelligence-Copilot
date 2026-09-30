from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_document_query():
    response = client.post("/api/query", json={"question":"What is the enterprise refund policy?"})
    assert response.status_code == 200
    body = response.json()
    assert body["intent"] == "document"
    assert body["sources"]
