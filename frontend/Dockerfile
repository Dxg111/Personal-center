# 构建阶段
FROM node:22-alpine AS builder

LABEL maintainer="your-email@example.com"
LABEL description="Personal Center Frontend"

WORKDIR /app

# 可通过构建参数切换 npm 源（默认官方源）
ARG NPM_REGISTRY=https://registry.npmjs.org/

# 复制依赖文件（必须包含 package-lock.json）
COPY package*.json ./

# 构建阶段需要 devDependencies（vite 在 devDependencies 中）
RUN npm ci --no-audit --no-fund \
    --registry=${NPM_REGISTRY} \
    --fetch-retries=5 \
    --fetch-retry-maxtimeout=120000

# 复制源代码
COPY . .

# 构建
RUN npm run build

# 生产阶段
FROM nginx:alpine

# 复制构建产物
COPY --from=builder /app/dist /usr/share/nginx/html

# 复制 Nginx 配置
COPY nginx.conf /etc/nginx/conf.d/default.conf

# 暴露端口
EXPOSE 80

# 健康检查（显式使用 IPv4，避免 localhost 解析到 IPv6）
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD wget -q -O /dev/null http://127.0.0.1/ || exit 1

# 启动 Nginx
CMD ["nginx", "-g", "daemon off;"]
