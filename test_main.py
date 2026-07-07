from fastapi.testclient import TestClient

from main import app


def test_shorten_and_redirect():
    # dung 'with' de FastAPI chay lifespan (init_db) truoc khi test
    with TestClient(app) as client:
        resp = client.post("/shorten", json={"url": "https://example.com"})
        assert resp.status_code == 200
        code = resp.json()["code"]

        resp = client.get(f"/{code}", follow_redirects=False)
        assert resp.status_code == 307
        assert resp.headers["location"] == "https://example.com"


def test_unknown_code_returns_404():
    with TestClient(app) as client:
        resp = client.get("/khong-ton-tai", follow_redirects=False)
        assert resp.status_code == 404