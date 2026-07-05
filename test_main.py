from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_shorten_and_redirect():
    # Tạo mã ngắn, rồi kiểm tra nó redirect đúng chỗ.
    resp = client.post("/shorten", json={"url": "https://example.com"})
    assert resp.status_code == 200
    code = resp.json()["code"]

    resp = client.get(f"/{code}", follow_redirects=False)
    assert resp.status_code == 307
    assert resp.headers["location"] == "https://example.com"


def test_unknown_code_returns_404():
    # Mã không tồn tại thì phải trả 404.
    resp = client.get("/khong-ton-tai", follow_redirects=False)
    assert resp.status_code == 404