![CI](https://github.com/<user>/snip/actions/workflows/ci.yml/badge.svg)

# snip — Project 1 (Beginner)

URL shortener nhỏ, được đưa từ máy local lên **một server Linux thật**, đóng gói
bằng Docker, có CI cơ bản. Đây là level đầu của lộ trình 3 project — mục tiêu:
chạy end-to-end như một dịch vụ thật.

**Tech:** Python (FastAPI) · SQLite · Docker · GitHub Actions · EC2

---

## Trạng thái các phase

- [x] **Phase 1 — Chạy tay:** app chạy local bằng `uvicorn`
- [x] **Phase 2 — Đóng gói:** Docker + volume giữ dữ liệu
- [x] **Phase 3 — Lên server:** deploy lên EC2, mở port public, tự chạy lại sau reboot
- [x] **Phase 4 — Tự động:** GitHub Actions build + test mỗi lần push

**Definition of done (đạt đủ):** push code → CI chạy test ✅ · người ngoài vào
được URL public ✅ · server reboot thì app tự sống lại ✅

---

## Kiến trúc hiện tại

```
[Người dùng] --HTTP:80--> [EC2] --docker -p 80:8000--> [container snip] --> [volume: snip-data]
```

Một server, một container, dữ liệu trong SQLite nằm trên Docker volume.

## API

| Method | Path       | Việc                                |
|--------|------------|-------------------------------------|
| POST   | `/shorten` | `{"url": "..."}` -> tra ma ngan     |
| GET    | `/{code}`  | Redirect 307 ve URL goc, hoac 404   |
| GET    | `/docs`    | Giao dien thu API cua FastAPI       |

---

## Chạy local

```bash
pip install -r requirements.txt
uvicorn main:app --reload      # http://127.0.0.1:8000/docs
pytest -q                      # chạy test
```

## Chạy bằng Docker

```bash
docker build -t snip .
docker run -d --name snip -p 80:8000 -v snip-data:/app/data --restart unless-stopped snip
```

`--restart unless-stopped` để container tự chạy lại khi server reboot. Volume
`snip-data` giữ `data/snip.db` sống sót qua các lần xoá/tạo container.

---

## Quy trình làm việc (dev -> prod)

**1. Code qua nhánh + Pull Request (không push thẳng nhánh chính):**
```bash
git checkout -b fix-something
# sửa code...
git add .
git commit -m "fix: mo ta ngan gon"
git push -u origin fix-something
```
Mở PR vào `project-1-beginner` -> CI tự chạy test + build -> xanh mới merge.

**2. Đưa code mới lên server (thủ công ở level này):**
```bash
ssh user@<IP>
cd snip
git pull
docker build -t snip .
docker stop snip && docker rm snip
docker run -d --name snip -p 80:8000 -v snip-data:/app/data --restart unless-stopped snip
```

**3. Smoke test sau deploy:**
```bash
docker ps && docker logs snip
curl -s -o /dev/null -w "%{http_code}\n" localhost:80/docs   # 200
curl -s -X POST localhost:80/shorten -H "Content-Type: application/json" -d '{"url":"https://anthropic.com"}'
curl -i localhost:80/<code>                                  # 307 + location
curl -i http://<IP>/<code>                                   # test tu may ngoai
```

---

## Vận hành cơ bản (day-2)

| Việc | Lệnh |
|------|------|
| Xem log | `docker logs -f snip` |
| Xem trạng thái | `docker ps` |
| Restart | `docker restart snip` |
| Backup DB | `docker run --rm -v snip-data:/data -v $(pwd):/backup alpine cp /data/snip.db /backup/` |
| Cập nhật app | `git pull && docker build -t snip . && docker stop snip && docker rm snip && docker run -d ...` |

---

## Điểm gãy & hướng cải thiện

Những giới hạn *có chủ đích* của level này — mỗi cái là lý do tồn tại của một
công cụ ở Project 2/3:

| # | Điểm gãy hiện tại | Rủi ro | Cải thiện ở đâu |
|---|-------------------|--------|-----------------|
| 1 | **Deploy thủ công** (SSH + `git pull` + build tay) | Quên bước, sai lệnh, code mới không lên | Pipeline deploy (P2) |
| 2 | **SQLite** — 1 container mới dùng được | Không scale ngang, không backup tự động | Postgres (P2) |
| 3 | **1 server duy nhất** (SPOF) | Server chết = app chết | Nhiều node / K8s (P3) |
| 4 | **Không có HTTPS** — HTTP cổng 80 trần | Không mã hoá | TLS / Ingress (P3) |
| 5 | **Image chứa cả đồ test** (`pytest`, `httpx`) | Image phình, bề mặt tấn công lớn hơn | Multi-stage build (P2) |
| 6 | **Hạ tầng bấm tay** (EC2, Security Group qua Console) | Không tái lập, dễ lệch | Terraform (P2) |
| 7 | **Cấu hình server bằng tay** (SSH gõ lệnh cài Docker) | Không nhất quán giữa các server | Ansible (P2) |
| 8 | **Build image trên server** | Tốn tài nguyên server, không có nơi lưu image | ECR + build trong CI (P2) |
| 9 | **Không giám sát** | Không biết traffic, lỗi, latency | Prometheus + Grafana (P2) |
| 10 | **Downtime khi deploy** (stop -> rm -> run có khoảng chết) | App ngừng vài giây mỗi lần deploy | Rolling update (P3) |

---

## Bài học rút ra

- **Thứ tự COPY trong Dockerfile** quyết định tốc độ build (layer cache).
- **`--host 0.0.0.0`** bắt buộc để nghe được từ ngoài container.
- **`EXPOSE` không mở port** — port mở là do `-p` và Security Group/firewall.
- Mở được app từ ngoài cần thông **cả 3 lớp**: Docker `-p`, `ufw`, Security Group.
- **Vòng đời dữ liệu ≠ vòng đời container** -> cần volume.
- **CI môi trường sạch phơi bày bug "chạy máy tôi thì được"** — ví dụ app phải tự
  tạo thư mục `data/`, không giả định nó có sẵn.
- **CI xanh ≠ đã deploy** — ở level này build/test và deploy là hai việc tách rời.

---

## Tiếp theo -> Project 2

Biến snip thành hệ nhiều thành phần, dựng hạ tầng bằng code, có pipeline thật và
giám sát. Xem nhánh `project-2-intermediate`.