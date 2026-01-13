"""
GitHub Contributions Auto Commit System
Tạo các commit tự động để làm đẹp biểu đồ contributions
"""

import os
import random
import subprocess
from datetime import datetime, timedelta
import json

# ==================== CẤU HÌNH ====================
CONFIG = {
    # GitHub repository URL (thay bằng URL repo của bạn)
    "github_repo": "https://github.com/YOUR_USERNAME/YOUR_REPO.git",
    
    # Số commit tối thiểu và tối đa mỗi ngày
    "min_commits_per_day": 1,
    "max_commits_per_day": 5,
    
    # Ngày bắt đầu và kết thúc (format: YYYY-MM-DD)
    "start_date": "2024-01-01",
    "end_date": "2025-12-31",
    
    # Chỉ commit vào các ngày trong tuần (0=Monday, 6=Sunday)
    # Để None nếu muốn commit tất cả các ngày
    "weekdays_only": None,  # Ví dụ: [0, 1, 2, 3, 4] cho Mon-Fri
    
    # Pattern cho contributions (tùy chọn)
    # "random" - ngẫu nhiên
    # "wave" - dạng sóng
    # "consistent" - đều đặn
    "pattern": "random",
    
    # Tỷ lệ ngày có commit (0.0 - 1.0)
    "commit_probability": 0.7,
}

# File để ghi commit
COMMIT_FILE = "contributions.txt"


def run_command(command, env=None):
    """Chạy command và trả về output"""
    result = subprocess.run(
        command,
        shell=True,
        capture_output=True,
        text=True,
        env=env
    )
    return result.returncode, result.stdout, result.stderr


def init_git_repo():
    """Khởi tạo git repo nếu chưa có"""
    if not os.path.exists(".git"):
        run_command("git init")
        print("✓ Đã khởi tạo Git repository")
    else:
        print("✓ Git repository đã tồn tại")


def create_commit(date, message):
    """Tạo một commit với ngày cụ thể"""
    # Format date cho git
    date_str = date.strftime("%Y-%m-%d %H:%M:%S")
    
    # Ghi nội dung vào file
    with open(COMMIT_FILE, "a", encoding="utf-8") as f:
        f.write(f"Commit on {date_str}: {message}\n")
    
    # Stage file
    run_command(f"git add {COMMIT_FILE}")
    
    # Tạo commit với ngày tùy chỉnh
    env = os.environ.copy()
    env["GIT_AUTHOR_DATE"] = date_str
    env["GIT_COMMITTER_DATE"] = date_str
    
    commit_cmd = f'git commit -m "{message}"'
    returncode, stdout, stderr = run_command(commit_cmd, env=env)
    
    return returncode == 0


def get_commits_count(date, pattern):
    """Xác định số commit cho một ngày dựa trên pattern"""
    min_commits = CONFIG["min_commits_per_day"]
    max_commits = CONFIG["max_commits_per_day"]
    
    if pattern == "random":
        return random.randint(min_commits, max_commits)
    
    elif pattern == "wave":
        # Tạo dạng sóng dựa trên ngày trong tuần
        day_of_week = date.weekday()
        wave_values = [3, 4, 5, 4, 3, 2, 1]  # Mon -> Sun
        base = wave_values[day_of_week]
        return min(max(base + random.randint(-1, 1), min_commits), max_commits)
    
    elif pattern == "consistent":
        # Số commit đều đặn với variation nhỏ
        avg = (min_commits + max_commits) // 2
        return avg + random.randint(-1, 1)
    
    return random.randint(min_commits, max_commits)


def should_commit_today(date):
    """Kiểm tra xem có nên commit vào ngày này không"""
    # Kiểm tra weekdays_only
    if CONFIG["weekdays_only"] is not None:
        if date.weekday() not in CONFIG["weekdays_only"]:
            return False
    
    # Kiểm tra probability
    return random.random() < CONFIG["commit_probability"]


def generate_message(date, index):
    """Tạo commit message"""
    messages = [
        "Update contributions",
        "Daily update",
        "Add new content",
        "Improve documentation", 
        "Fix minor issues",
        "Code refactoring",
        "Update README",
        "Add new features",
        "Performance improvements",
        "Bug fixes",
        "Update dependencies",
        "Clean up code",
    ]
    return f"{random.choice(messages)} - {date.strftime('%Y-%m-%d')} #{index}"


def main():
    """Hàm chính"""
    print("=" * 50)
    print("🚀 GitHub Contributions Auto Commit System")
    print("=" * 50)
    
    # Khởi tạo repo
    init_git_repo()
    
    # Parse dates
    start_date = datetime.strptime(CONFIG["start_date"], "%Y-%m-%d")
    end_date = datetime.strptime(CONFIG["end_date"], "%Y-%m-%d")
    
    print(f"\n📅 Khoảng thời gian: {CONFIG['start_date']} -> {CONFIG['end_date']}")
    print(f"📊 Pattern: {CONFIG['pattern']}")
    print(f"🎲 Xác suất commit: {CONFIG['commit_probability'] * 100}%")
    print(f"📝 Commits/ngày: {CONFIG['min_commits_per_day']} - {CONFIG['max_commits_per_day']}")
    
    # Tạo file ban đầu nếu chưa có
    if not os.path.exists(COMMIT_FILE):
        with open(COMMIT_FILE, "w", encoding="utf-8") as f:
            f.write("# GitHub Contributions Log\n\n")
    
    # Đếm số commit
    total_commits = 0
    days_with_commits = 0
    
    current_date = start_date
    while current_date <= end_date:
        if should_commit_today(current_date):
            num_commits = get_commits_count(current_date, CONFIG["pattern"])
            
            for i in range(num_commits):
                # Thêm random time trong ngày
                random_hour = random.randint(8, 22)
                random_minute = random.randint(0, 59)
                commit_time = current_date.replace(hour=random_hour, minute=random_minute)
                
                message = generate_message(current_date, i + 1)
                if create_commit(commit_time, message):
                    total_commits += 1
            
            days_with_commits += 1
            print(f"✓ {current_date.strftime('%Y-%m-%d')}: {num_commits} commits")
        
        current_date += timedelta(days=1)
    
    print("\n" + "=" * 50)
    print(f"✅ Hoàn thành!")
    print(f"📊 Tổng số commits: {total_commits}")
    print(f"📅 Số ngày có commit: {days_with_commits}")
    print("=" * 50)
    
    return total_commits, days_with_commits


def setup_and_push():
    """Setup remote và push lên GitHub"""
    repo_url = CONFIG['github_repo']
    
    print(f"\n🔗 Đang kết nối với: {repo_url}")
    
    # Kiểm tra xem remote đã tồn tại chưa
    returncode, stdout, stderr = run_command("git remote get-url origin")
    
    if returncode == 0:
        # Remote đã tồn tại, cập nhật URL
        print("   Remote 'origin' đã tồn tại, đang cập nhật...")
        run_command(f"git remote set-url origin {repo_url}")
    else:
        # Thêm remote mới
        run_command(f"git remote add origin {repo_url}")
    
    # Đổi tên branch thành main
    run_command("git branch -M main")
    
    print("📤 Đang push lên GitHub...")
    returncode, stdout, stderr = run_command("git push -u origin main --force")
    
    if returncode == 0:
        print("\n" + "=" * 50)
        print("🎉 PUSH THÀNH CÔNG!")
        print("=" * 50)
        print(f"\n👉 Xem contributions tại: {repo_url.replace('.git', '')}")
        print("   (Có thể mất vài phút để GitHub cập nhật)")
    else:
        print("\n❌ Push thất bại!")
        print(f"   Lỗi: {stderr}")
        print("\n💡 Hãy thử chạy thủ công:")
        print(f"   git remote add origin {repo_url}")
        print("   git branch -M main")
        print("   git push -u origin main --force")


def reset_repo():
    """Xóa tất cả commits và reset repo về trạng thái ban đầu"""
    print("\n" + "=" * 50)
    print("🗑️  XÓA TẤT CẢ COMMITS")
    print("=" * 50)
    
    # Kiểm tra có phải git repo không
    if not os.path.exists(".git"):
        print("❌ Không tìm thấy Git repository!")
        return False
    
    # Hiển thị số commits hiện tại
    returncode, stdout, stderr = run_command("git rev-list --count HEAD")
    if returncode == 0:
        print(f"📊 Số commits hiện tại: {stdout.strip()}")
    
    confirm = input("\n⚠️  Bạn có chắc muốn XÓA TẤT CẢ commits? (yes/no): ")
    
    if confirm.lower() != 'yes':
        print("❌ Đã hủy.")
        return False
    
    print("\n🔄 Đang xóa...")
    
    # Xóa thư mục .git
    import shutil
    try:
        shutil.rmtree(".git")
        print("✓ Đã xóa .git folder")
    except Exception as e:
        print(f"❌ Lỗi khi xóa .git: {e}")
        return False
    
    # Xóa file contributions.txt nếu có
    if os.path.exists(COMMIT_FILE):
        os.remove(COMMIT_FILE)
        print(f"✓ Đã xóa {COMMIT_FILE}")
    
    print("\n✅ Đã reset repo thành công!")
    print("   Bạn có thể chạy lại script để tạo commits mới.")
    
    # Hỏi có muốn push empty repo lên GitHub không
    push_confirm = input("\n🚀 Bạn có muốn xóa commits trên GitHub luôn không? (y/n): ")
    
    if push_confirm.lower() == 'y':
        # Khởi tạo repo mới với 1 commit rỗng
        run_command("git init")
        with open("README.md", "w") as f:
            f.write("# Contributions\n")
        run_command("git add README.md")
        run_command('git commit -m "Initial commit"')
        run_command("git branch -M main")
        
        repo_url = CONFIG['github_repo']
        run_command(f"git remote add origin {repo_url}")
        
        print("📤 Đang push repo rỗng lên GitHub...")
        returncode, stdout, stderr = run_command("git push -u origin main --force")
        
        if returncode == 0:
            print("✅ Đã xóa commits trên GitHub!")
        else:
            print(f"❌ Push thất bại: {stderr}")
    
    return True


def preview():
    """Xem trước số commit sẽ được tạo"""
    print("=" * 50)
    print("👀 PREVIEW - Xem trước commits sẽ được tạo")
    print("=" * 50)
    
    start_date = datetime.strptime(CONFIG["start_date"], "%Y-%m-%d")
    end_date = datetime.strptime(CONFIG["end_date"], "%Y-%m-%d")
    
    total_commits = 0
    days_with_commits = 0
    
    # Lưu trạng thái random để preview chính xác
    random.seed(42)
    
    current_date = start_date
    while current_date <= end_date:
        if should_commit_today(current_date):
            num_commits = get_commits_count(current_date, CONFIG["pattern"])
            total_commits += num_commits
            days_with_commits += 1
        current_date += timedelta(days=1)
    
    # Reset seed để khi chạy thật sẽ random khác
    random.seed()
    
    total_days = (end_date - start_date).days + 1
    
    print(f"\n📅 Tổng số ngày: {total_days}")
    print(f"📅 Ngày có commit: {days_with_commits}")
    print(f"📊 Tổng commits dự kiến: {total_commits}")
    print(f"📈 Trung bình commits/ngày: {total_commits / max(days_with_commits, 1):.1f}")
    print(f"🔗 GitHub repo: {CONFIG['github_repo']}")
    
    return total_commits, days_with_commits


if __name__ == "__main__":
    import sys
    
    # Kiểm tra argument
    if len(sys.argv) > 1:
        if sys.argv[1] == "reset":
            reset_repo()
            sys.exit(0)
        elif sys.argv[1] == "push":
            setup_and_push()
            sys.exit(0)
    
    print("\n" + "=" * 50)
    print("🚀 GitHub Contributions Auto Commit System")
    print("=" * 50)
    print("⚠️  Script này sẽ tạo nhiều commits trong git history.")
    print("⚠️  Chỉ nên dùng cho repo riêng, không dùng cho dự án thật.")
    print("\n💡 Các lệnh khác:")
    print("   python auto_commit.py reset  - Xóa tất cả commits")
    print("   python auto_commit.py push   - Push lên GitHub")
    
    # Bước 1: Xem preview
    print("\n" + "-" * 50)
    preview()
    
    # Bước 2: Hỏi có muốn tạo commits không
    print("\n" + "-" * 50)
    confirm = input("\n🤔 Bạn có muốn tạo commits? (y/n): ")
    
    if confirm.lower() != 'y':
        print("❌ Đã hủy.")
        sys.exit(0)
    
    # Bước 3: Chạy tạo commits
    total_commits, days_with_commits = main()
    
    # Bước 4: Hỏi có muốn push lên GitHub không
    print("\n" + "-" * 50)
    push_confirm = input("\n🚀 Bạn có muốn push lên GitHub ngay bây giờ? (y/n): ")
    
    if push_confirm.lower() == 'y':
        setup_and_push()
    else:
        print("\n📝 Để push sau, chạy lệnh:")
        print(f"   git remote add origin {CONFIG['github_repo']}")
        print("   git branch -M main")
        print("   git push -u origin main --force")
