FROM python:3.11-slim

LABEL maintainer="your-email@example.com"
LABEL description="Personal Center Backend API"

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# 健康检查需要 curl；PyMySQL / cryptography / bcrypt 均有预编译 wheel
RUN apt-get update && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

# 安装 Python 依赖
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# 复制应用代码（.dockerignore 已排除 .env / 测试 / 上传文件）
COPY . .

# 创建非 root 运行用户和上传目录
RUN useradd --create-home --uid 10001 appuser \
    && mkdir -p uploads \
    && chown -R appuser:appuser /app

USER appuser

# 健康检查不依赖数据库，避免首次迁移前一直 unhealthy
HEALTHCHECK --interval=30s --timeout=10s --start-period=20s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]
