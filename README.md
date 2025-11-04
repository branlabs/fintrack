# FinTrack

> Ghi chép chi tiêu hằng ngày theo danh mục và xem biểu đồ trực quan.

## Tính năng

* Ghi nhanh chi tiêu theo **danh mục**
* Quản lý **ngân sách** theo **tuần / tháng / năm**
* **Biểu đồ** theo **ngày / tuần / tháng**
* Xuất báo cáo: **PDF**, **CSV**

## Kiến trúc

* `fintrack/web` — Ứng dụng web (Bootstrap)
* `fintrack/api/v1` — REST API (Django)

> Không dùng monorepo. Toàn bộ mã nguồn nằm trong thư mục gốc `fintrack/` để đơn giản hoá.

## Yêu cầu

* Python **3.10+**
* `pip` mới nhất (khuyến nghị)
* Git

## Cài đặt & Chạy

### macOS / Linux

```bash
# 1) Clone source and create the virtual environment
git clone https://github.com/brandlabs/fintrack.git
cd fintrack
python -m venv .venv
source .venv/bin/activate

# 2) Install packages
python -m pip install --upgrade pip
pip install django  

# 3) Initial Database 
python .\manage.py migrate

# 4) Run server
python .\manage.py runserver
```

### Windows (PowerShell)

```powershell
# 1) Clone source and create the virtual environment
git clone https://github.com/brandlabs/fintrack.git
cd fintrack
python -m venv .venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1

# 2) Install packages
python -m pip install --upgrade pip
pip install django  

# 3) Initial Database 
python .\manage.py migrate

# 4) Run server
python .\manage.py runserver
```

## Cấu trúc thư mục (dự kiến)

```
fintrack/
├─ web/                 # source web (templates, static, Bootstrap)
├─ api/
│  └─ v1/               # Django REST API (views, serializers, urls)
├─ manage.py
```

