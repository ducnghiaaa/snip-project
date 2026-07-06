import secrets
import sqlite3
import os

from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel

DB_PATH = "data/snip.db"

app = FastAPI(title="Snip API")


def init_db():
    d = os.path.dirname(DB_PATH)
    if d:
        os.makedirs(d, exist_ok=True)
    # Tao bang luu URL neu chua co. Chay mot lan luc app khoi dong
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            "CREATE TABLE IF NOT EXISTS urls ("
            "  code TEXT PRIMARY KEY,"
            "  long_url TEXT NOT NULL"
            ")"
        )

init_db()
os.makedirs("data", exist_ok=True)

class ShortenRequest(BaseModel):
    # Dinh nghia "body" ma client phai gui len
    url: str
    
@app.post("/shorten")
def shorten(req: ShortenRequest):
    # Nhận URL dài -> sinh mã ngắn ngẫu nhiên -> lưu vào DB -> trả mã về.
    code = secrets.token_urlsafe(4)
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            "INSERT INTO urls (code, long_url) VALUES (?, ?)",
            (code, req.url),
        )
    return {"code": code, "short_url": f"/{code}"}

@app.get("/{code}")
def redirect(code: str):
    # Nhận mã ngắn -> tra DB -> redirect sang URL dài (hoặc 404 nếu không có).
    with sqlite3.connect(DB_PATH) as conn:
        row = conn.execute(
            "SELECT long_url FROM urls WHERE code = ?", (code,)
        ).fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Khong tim thay ma")
    return RedirectResponse(url=row[0], status_code=307)