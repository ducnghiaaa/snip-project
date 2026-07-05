FROM python:3.12-slim

WORKDIR /app

# Copy requirement truoc, cai truoc -> tan dung cache cua Docker layer
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy code vao sau cung vi no thay doi thuong xuyen
COPY main.py .

EXPOSE 8000

# Trong container khong dung --reload. Bind 0.0.0.0 de nghe tu ben ngoai container
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]