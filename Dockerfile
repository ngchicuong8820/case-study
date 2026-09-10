# --- STAGE 1: Build & Dependencies Stage ---
FROM python:3.9-slim AS builder

WORKDIR /app

# Cài đặt các công cụ phục vụ build nếu cần
RUN apt-get update && apt-get install -y --no-install-recommends gcc

# Cài đặt thư viện phụ thuộc vào thư mục tạm
COPY app/requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# --- STAGE 2: Production Runtime Stage ---
FROM python:3.9-slim AS runtime

WORKDIR /app

# Chỉ copy các thư viện đã được cài đặt từ stage builder sang, loại bỏ hoàn toàn trình biên dịch (gcc)
COPY --from=builder /root/.local /root/.local
COPY . /app

# Khai báo biến môi trường cho python path
ENV PATH=/root/.local/bin:$PATH

# Khai báo user phi root để vá lỗi bảo mật container chạy quyền root (đã phát hiện ở Task 1)
RUN useradd -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 5000
CMD ["python", "app.py"]