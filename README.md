# snip — DevOps Learning Journey

Một URL shortener nhỏ (`POST` URL dài → mã ngắn; `GET` mã ngắn → redirect), được
vận hành lại qua **3 mức độ trưởng thành** theo phương pháp xoắn ốc.

> **Cùng một app, ba lớp vận hành.** Mỗi level không làm lại từ đầu — nó phủ thêm
> một lớp hạ tầng/tự động hoá lên cùng ứng dụng, nên kiến thức cũ được dùng lại
> liên tục.

---

## Ba level

| Level | Nhánh | Nội dung | Trạng thái |
|-------|-------|----------|:----------:|
| 🟢 **1. Beginner** | [`project-1-beginner`](../../tree/project-1-beginner) | App + Docker + deploy 1 server + CI cơ bản | 🚧 Đang làm |
| 🟡 **2. Intermediate** | `project-2-intermediate` | Multi-service (Postgres/Redis) + Terraform + Ansible + Prometheus | ⏳ Chưa bắt đầu |
| 🔴 **3. Advanced** | `project-3-advanced` | Kubernetes (EKS) + GitOps (ArgoCD) + observability đầy đủ | ⏳ Chưa bắt đầu |

*(Cập nhật link nhánh theo tên repo thật của bạn nếu đường dẫn tương đối không hoạt động.)*

---

## Vì sao làm theo cách này

- **Xoắn ốc:** mỗi level ôn lại toàn bộ nền của level trước ở tầng sâu hơn — học
  tới đâu ôn lại tới đó, khó quên.
- **URL shortener:** đủ nhỏ để không ngợp, nhưng tự sinh traffic (lượt redirect)
  → nguyên liệu thật để tập giám sát ở level sau.

## Cách xem repo

Chọn nhánh tương ứng với level bạn muốn xem; mỗi nhánh có README riêng mô tả chi
tiết từng phase của level đó.

## Tech theo level

- **Level 1:** Python (FastAPI), Docker, Linux, Git, GitHub Actions, EC2
- **Level 2:** Docker Compose, Postgres, Redis, Terraform, Ansible, ECR, Prometheus, Grafana
- **Level 3:** Kubernetes, EKS, Helm, ArgoCD, Prometheus stack đầy đủ
