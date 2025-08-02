# --- Giai đoạn 1: Builder ---
# Dùng Node.js để build code Vue thành các file tĩnh
FROM node:18-alpine AS builder

# Cài đặt các công cụ build cần thiết cho các gói native
RUN apk add --no-cache build-base python3

# Đặt thư mục làm việc
WORKDIR /app

# Copy file package.json và cài đặt thư viện
COPY package*.json ./
RUN npm install

# Copy toàn bộ source code
COPY . .

# Chạy lệnh build để tạo ra thư mục "dist" chứa sản phẩm cuối cùng
RUN npm run build

# --- Giai đoạn 2: Final Image ---
# Bắt đầu từ một image nginx siêu nhẹ để phục vụ web
FROM nginx:stable-alpine

# Copy sản phẩm đã build từ thư mục /app/dist của giai đoạn "builder"
# vào thư mục mặc định của nginx để phục vụ web
COPY --from=builder /app/dist /usr/share/nginx/html

# Mở port 80 của nginx
EXPOSE 80

# Lệnh để khởi động server nginx
CMD ["nginx", "-g", "daemon off;"]