# GitHub Contributions Auto Commit System

🎨 Hệ thống tự động tạo commits để làm đẹp biểu đồ contributions trên GitHub.

## 📋 Yêu cầu

- Python 3.6+
- Git đã được cài đặt và cấu hình
- Tài khoản GitHub

## 🚀 Cách sử dụng

### 1. Clone repo

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git
cd YOUR_REPO
```

### 2. Cấu hình

Mở file `auto_commit.py` và chỉnh sửa phần `CONFIG`:

```python
CONFIG = {
    # Thay bằng URL repo của bạn
    "github_repo": "https://github.com/YOUR_USERNAME/YOUR_REPO.git",

    # Số commit tối thiểu và tối đa mỗi ngày
    "min_commits_per_day": 1,
    "max_commits_per_day": 5,

    # Ngày bắt đầu và kết thúc
    "start_date": "2024-01-01",
    "end_date": "2025-12-31",

    # Pattern: "random", "wave", "consistent"
    "pattern": "random",

    # Tỷ lệ ngày có commit (0.0 - 1.0)
    "commit_probability": 0.7,
}
```

### 2. Xem trước

Chạy lệnh để xem trước số commits sẽ được tạo:

```bash
python auto_commit.py preview
```

### 3. Chạy script

```bash
python auto_commit.py
```

### 4. Kết nối với GitHub

```bash
# Bước 1: Tạo repo MỚI trên GitHub (KHÔNG tick "Add README")

# Bước 2: Kết nối repo local với GitHub
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git

# Bước 3: Đẩy code lên
git branch -M main
git push -u origin main --force
```

> ⚠️ **Lưu ý**: Sử dụng `--force` sẽ ghi đè toàn bộ lịch sử commit trên remote!

## 📊 Các Pattern

| Pattern      | Mô tả                                             |
| ------------ | ------------------------------------------------- |
| `random`     | Số commits ngẫu nhiên mỗi ngày                    |
| `wave`       | Nhiều commits hơn vào giữa tuần, ít hơn cuối tuần |
| `consistent` | Số commits đều đặn mỗi ngày                       |

## ⚙️ Tùy chọn nâng cao

### Chỉ commit vào ngày trong tuần

```python
"weekdays_only": [0, 1, 2, 3, 4]  # Monday to Friday
```

### Điều chỉnh xác suất

```python
"commit_probability": 0.5  # 50% ngày sẽ có commit
```

## ⚠️ Lưu ý

- Chỉ sử dụng cho repo cá nhân
- Không sử dụng cho các dự án thật
- GitHub có thể detect và không hiển thị contributions giả

## 📝 License

MIT License
