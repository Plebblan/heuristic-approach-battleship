#!/bin/bash

# 1. Tạo môi trường ảo tên là 'env'
python3 -m venv env

# 2. Kích hoạt môi trường ảo
source env/bin/activate

# 3. Nâng cấp pip
pip install --upgrade pip

# 4. Cài đặt các thư viện từ file requirements.txt
if [ -f requirements.txt ]; then
    pip install -r requirements.txt
    echo "✅ Đã cài đặt xong các thư viện."
else
    echo "❌ Không tìm thấy file requirements.txt"
fi

echo "------------------------------------------------"
echo "🔥 Để bắt đầu, hãy gõ: source env/bin/activate"
echo "------------------------------------------------"