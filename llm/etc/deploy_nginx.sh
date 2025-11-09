#!/bin/bash

# --- deploy_nginx.sh ---
# Script để tự động kích hoạt một config Nginx mới
# và khởi động lại Nginx.

# Tên file config của bạn (thay đổi nếu cần)
CONFIG_NAME="llm_gateway.conf"

# Đường dẫn đầy đủ
AVAILABLE_PATH="/etc/nginx/sites-available/$CONFIG_NAME"
ENABLED_PATH="/etc/nginx/sites-enabled/$CONFIG_NAME"
DEFAULT_PATH="/etc/nginx/sites-enabled/default"

# Dừng script ngay nếu có lỗi
set -e

# --- BƯỚC 1: KÍCH HOẠT CONFIG MỚI ---
# Kiểm tra xem file config có tồn tại không
if [ ! -f "$AVAILABLE_PATH" ]; then
    echo "Lỗi: Không tìm thấy file config tại $AVAILABLE_PATH"
    exit 1
fi

# Kiểm tra xem nó đã được kích hoạt chưa
if [ -L "$ENABLED_PATH" ]; then
    echo "Thông báo: Config $CONFIG_NAME đã được kích hoạt."
else
    echo "Kích hoạt $CONFIG_NAME..."
    sudo ln -s "$AVAILABLE_PATH" "$ENABLED_PATH"
fi

# --- BƯỚC 2: VÔ HIỆU HÓA CONFIG MẶC ĐỊNH ---
if [ -L "$DEFAULT_PATH" ]; then
    echo "Vô hiệu hóa config Nginx mặc định..."
    sudo rm "$DEFAULT_PATH"
else
    echo "Thông báo: Config mặc định đã được vô hiệu hóa."
fi

# --- BƯỚC 3: KIỂM TRA VÀ KHỞI ĐỘNG LẠI ---
echo "Kiểm tra cú pháp Nginx..."
sudo nginx -t

# Nếu lệnh trên thất bại, 'set -e' sẽ dừng script ở đây.
# Nếu thành công, tiếp tục khởi động lại.

echo "Khởi động lại Nginx..."
sudo systemctl restart nginx

echo "Hoàn tất! Nginx đã được cập nhật với $CONFIG_NAME."