# FinTrack

> Daily expense— ghi chép chi và xem báo cáo trực quan.

## Tính năng
- Ghi nhanh thu/chi theo danh mục, ghi chú, ví/nguồn tiền
- Ngân sách theo tháng và cảnh báo khi sắp vượt ngưỡng
- Biểu đồ ngày/tuần/tháng, báo cáo theo danh mục & ví
- Tìm kiếm, lọc nâng cao; xuất CSV
- Đồng bộ đa thiết bị (tùy chọn), sao lưu/khôi phục dữ liệu
- Quyền riêng tư: dữ liệu cá nhân, có thể chạy hoàn toàn cục bộ

## Kiến trúc (đề xuất)
- `apps/web` – ứng dụng web (ví dụ: Next.js/React)
- `packages/api` – REST/GraphQL API (ví dụ: Node.js)
- `packages/db` – schema & migration (ví dụ: Prisma + PostgreSQL)
- `packages/ui` – thư viện UI dùng chung (nếu cần)

> Không dùng monorepo? Đơn giản giữ một app duy nhất trong root `fintrack/`.

## Bắt đầu
```bash
# 1) Clone
git clone https://github.com/<your-org-or-user>/fintrack
cd fintrack

# 2) Cấu hình
cp .env.example .env   # cập nhật DATABASE_URL, JWT_SECRET, v.v.

# 3) Cài đặt & chạy (ví dụ với pnpm)
pnpm install
pnpm dev
