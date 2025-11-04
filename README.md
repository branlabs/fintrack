# FinTrack

> Daily expense — ghi chép danh mục chi mỗi ngày và hiển thị báo cáo trực quan.

## Tính năng
- Ghi nhanh thu/chi theo danh mục, ghi chú, ví/nguồn tiền
- Ngân sách theo tháng và cảnh báo khi sắp vượt ngưỡng
- Biểu đồ ngày/tuần/tháng, báo cáo theo danh mục & ví
- Tìm kiếm, lọc nâng cao; xuất CSV
- Đồng bộ đa thiết bị (tùy chọn), sao lưu/khôi phục dữ liệu
- Quyền riêng tư: dữ liệu cá nhân, có thể chạy hoàn toàn cục bộ

## Kiến trúc 
- `fintrack/web` – ứng dụng web (boostrap)
- `finctrack/api/v1` – REST API Django 


> Không dùng monorepo? Đơn giản giữ một app duy nhất trong root `fintrack/`.

## Bắt đầu
```bash
# 1) Create the virtual environment
git clone https//github.com/brandlabs/fintrack.git
python -m venv menv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
& .\fintrack-env\Scripts\Activate.ps1
cd fintrack

# 2) Install packages
pip install --pre django
python -m pip install --upgrade pip

# 3) Run webserver
python .\manage.py runserver
```