import os
import time
import secrets
from contextlib import contextmanager, asynccontextmanager

import psycopg2
import redis
from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from prometheus_fastapi_instrumentator import Instrumentator

DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://snip:snip@db:5432/snip")
REDIS_URL = os.environ.get("REDIS_URL", "redis://cache:6379/0")

cache = redis.Redis.from_url(REDIS_URL, decode_responses=True)


@contextmanager
def get_cursor(commit=False):
    conn = psycopg2.connect(DATABASE_URL)
    try:
        with conn.cursor() as cur:
            yield cur
        if commit:
            conn.commit()
    finally:
        conn.close()


def init_db():
    # Postgres co the chua san sang khi API khoi dong -> thu lai vai lan.
    for _ in range(10):
        try:
            with get_cursor(commit=True) as cur:
                cur.execute(
                    "CREATE TABLE IF NOT EXISTS urls ("
                    "  code TEXT PRIMARY KEY,"
                    "  long_url TEXT NOT NULL"
                    ")"
                )
            return
        except psycopg2.OperationalError:
            time.sleep(2)
    raise RuntimeError("Khong ket noi duoc Postgres")


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(title="snip", lifespan=lifespan)
Instrumentator().instrument(app).expose(app)  # phoi /metrics cho Prometheus


class ShortenRequest(BaseModel):
    url: str


@app.post("/shorten")
def shorten(req: ShortenRequest):
    code = secrets.token_urlsafe(4)
    with get_cursor(commit=True) as cur:
        cur.execute(
            "INSERT INTO urls (code, long_url) VALUES (%s, %s)",
            (code, req.url),
        )
    return {"code": code, "short_url": f"/{code}"}


@app.get("/{code}")
def redirect(code: str):
    long_url = cache.get(code)              # cache-aside: tra Redis truoc
    if long_url is None:
        with get_cursor() as cur:
            cur.execute("SELECT long_url FROM urls WHERE code = %s", (code,))
            row = cur.fetchone()
        if row is None:
            raise HTTPException(status_code=404, detail="Khong tim thay ma")
        long_url = row[0]
        cache.set(code, long_url, ex=3600)  # luu cache 1 gio
    return RedirectResponse(url=long_url, status_code=307)