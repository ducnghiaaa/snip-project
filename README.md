# snip — Project 1 (Beginner)

Một dịch vụ rút gọn URL nhỏ: gửi một URL dài, nhận lại mã ngắn; truy cập mã ngắn
thì được chuyển hướng về URL gốc. Project này đưa app từ máy cá nhân lên một
server thật trên Internet, đóng gói bằng Docker và có kiểm thử tự động.

**Công nghệ:** Python (FastAPI) · SQLite · Docker · GitHub Actions · AWS EC2

## Trạng thái

- [x] Chạy local bằng `uvicorn`
- [x] Đóng gói Docker + volume giữ dữ liệu
- [x] Deploy lên EC2, mở port public, tự chạy lại sau reboot
- [x] CI: mỗi lần push tự build + test

## Kiến trúc

```
Người dùng --HTTP:80--> EC2 --docker -p 80:8000--> container snip --> volume (SQLite)
```

## Chạy thử

```bash
# Local
pip install -r requirements.txt
uvicorn main:app --reload        # mở http://127.0.0.1:8000/docs

# Docker
docker build -t snip .
docker run -d --name snip -p 80:8000 -v snip-data:/app/data --restart unless-stopped snip
```

## Quy trình code

Không push thẳng nhánh chính: tạo nhánh mới → mở Pull Request → CI chạy test tự
động → xanh mới merge. Đưa lên server bằng `git pull` + build lại (thủ công ở
level này).

## Giới hạn hiện tại (sẽ vá ở Project 2)

| Giới hạn | Cách vá |
|----------|---------|
| Deploy thủ công qua SSH | Pipeline deploy tự động |
| SQLite chỉ 1 container dùng được | Postgres chạy như service riêng |
| Image chứa cả thư viện test | Multi-stage build cho image gọn |
| Hạ tầng bấm tay trên AWS Console | Terraform (hạ tầng bằng code) |
| Cấu hình server bằng SSH gõ tay | Ansible tự động hoá |
| Build image ngay trên server | Đẩy image lên ECR, server chỉ pull |
| Chưa có giám sát | Prometheus + Grafana |
| Sửa README cũng kích hoạt CI | Lọc trigger theo đường dẫn (bỏ qua `.md`) |

## Tiếp theo

Project 2 biến snip thành hệ nhiều thành phần, dựng hạ tầng bằng code và có giám
sát. Xem nhánh `project-2-intermediate`.