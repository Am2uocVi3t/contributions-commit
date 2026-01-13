"""
Tạo pattern hình ảnh trên GitHub contributions
Ví dụ: Tên, chữ, biểu tượng...
"""

import os
import random
import subprocess
from datetime import datetime, timedelta

# Pattern chữ (7 hàng x N cột, giống grid contributions của GitHub)
# 1 = có commit, 0 = không commit
# Mỗi cột là 1 tuần (7 ngày từ Sunday -> Saturday)

PATTERNS = {
    "LOVE": [
        # L       O       V       E
        [1,0,0,0,1,1,1,0,1,0,0,0,1,0,1,1,1,1],
        [1,0,0,0,1,0,0,1,1,0,0,0,1,0,1,0,0,0],
        [1,0,0,0,1,0,0,1,0,1,0,1,0,0,1,0,0,0],
        [1,0,0,0,1,0,0,1,0,1,0,1,0,0,1,1,1,0],
        [1,0,0,0,1,0,0,1,0,0,1,0,0,0,1,0,0,0],
        [1,0,0,0,1,0,0,1,0,0,1,0,0,0,1,0,0,0],
        [1,1,1,0,1,1,1,0,0,0,1,0,0,0,1,1,1,1],
    ],
    "HI": [
        [1,0,0,0,1,0,1,1,1],
        [1,0,0,0,1,0,0,1,0],
        [1,0,0,0,1,0,0,1,0],
        [1,1,1,1,1,0,0,1,0],
        [1,0,0,0,1,0,0,1,0],
        [1,0,0,0,1,0,0,1,0],
        [1,0,0,0,1,0,1,1,1],
    ],
    "HEART": [
        [0,1,1,0,0,1,1,0],
        [1,1,1,1,1,1,1,1],
        [1,1,1,1,1,1,1,1],
        [1,1,1,1,1,1,1,1],
        [0,1,1,1,1,1,1,0],
        [0,0,1,1,1,1,0,0],
        [0,0,0,1,1,0,0,0],
    ],
    "CODE": [
        [0,1,1,0,0,1,1,0,1,1,1,0,1,1,1],
        [1,0,0,0,1,0,0,1,1,0,0,1,1,0,0],
        [1,0,0,0,1,0,0,1,1,0,0,1,1,0,0],
        [1,0,0,0,1,0,0,1,1,0,0,1,1,1,0],
        [1,0,0,0,1,0,0,1,1,0,0,1,1,0,0],
        [1,0,0,0,1,0,0,1,1,0,0,1,1,0,0],
        [0,1,1,0,0,1,1,0,1,1,1,0,1,1,1],
    ],
}


def run_command(command, env=None):
    """Chạy command"""
    result = subprocess.run(
        command,
        shell=True,
        capture_output=True,
        text=True,
        env=env
    )
    return result.returncode == 0


def init_git_repo():
    """Khởi tạo git repo"""
    if not os.path.exists(".git"):
        run_command("git init")
        print("✓ Đã khởi tạo Git repository")


def create_commit(date, num_commits):
    """Tạo commits cho một ngày"""
    for i in range(num_commits):
        random_hour = random.randint(8, 22)
        random_minute = random.randint(0, 59)
        commit_time = date.replace(hour=random_hour, minute=random_minute)
        date_str = commit_time.strftime("%Y-%m-%d %H:%M:%S")
        
        with open("pattern.txt", "a", encoding="utf-8") as f:
            f.write(f"Pattern commit: {date_str}\n")
        
        run_command("git add pattern.txt")
        
        env = os.environ.copy()
        env["GIT_AUTHOR_DATE"] = date_str
        env["GIT_COMMITTER_DATE"] = date_str
        
        run_command(f'git commit -m "Update {date_str}"', env=env)


def create_pattern(pattern_name, start_date, commits_per_cell=4):
    """
    Tạo pattern trên contributions graph
    
    Args:
        pattern_name: Tên pattern (LOVE, HI, HEART, CODE)
        start_date: Ngày bắt đầu (phải là Sunday)
        commits_per_cell: Số commits cho mỗi ô có giá trị 1
    """
    if pattern_name not in PATTERNS:
        print(f"❌ Pattern '{pattern_name}' không tồn tại!")
        print(f"   Các pattern có sẵn: {list(PATTERNS.keys())}")
        return
    
    pattern = PATTERNS[pattern_name]
    
    print(f"🎨 Tạo pattern: {pattern_name}")
    print(f"📅 Ngày bắt đầu: {start_date}")
    
    init_git_repo()
    
    # Tạo file ban đầu
    with open("pattern.txt", "w", encoding="utf-8") as f:
        f.write(f"# Pattern: {pattern_name}\n")
    
    start = datetime.strptime(start_date, "%Y-%m-%d")
    
    # Đảm bảo start_date là Sunday
    if start.weekday() != 6:
        print("⚠️  Cảnh báo: start_date nên là Sunday để pattern hiển thị đúng")
    
    total_commits = 0
    num_weeks = len(pattern[0])
    
    for week in range(num_weeks):
        for day in range(7):  # 0=Sunday, 6=Saturday
            current_date = start + timedelta(weeks=week, days=day)
            
            if day < len(pattern) and week < len(pattern[day]):
                should_commit = pattern[day][week]
            else:
                should_commit = 0
            
            if should_commit:
                # Random số commits để tạo màu đậm/nhạt
                num = random.randint(commits_per_cell - 1, commits_per_cell + 2)
                create_commit(current_date, num)
                total_commits += num
                print(f"✓ {current_date.strftime('%Y-%m-%d')}: {num} commits")
    
    print(f"\n✅ Hoàn thành! Tổng: {total_commits} commits")


def preview_pattern(pattern_name):
    """Xem trước pattern"""
    if pattern_name not in PATTERNS:
        print(f"Pattern '{pattern_name}' không tồn tại!")
        return
    
    pattern = PATTERNS[pattern_name]
    
    print(f"\n📊 Preview pattern: {pattern_name}\n")
    
    for row in pattern:
        line = ""
        for cell in row:
            line += "██" if cell else "  "
        print(line)
    print()


if __name__ == "__main__":
    import sys
    
    print("=" * 50)
    print("🎨 GitHub Pattern Commit Generator")
    print("=" * 50)
    
    if len(sys.argv) < 2:
        print("\nCách sử dụng:")
        print("  python pattern_commit.py preview <pattern>  - Xem trước pattern")
        print("  python pattern_commit.py create <pattern> <start_date>")
        print("\nPatterns có sẵn:", list(PATTERNS.keys()))
        print("\nVí dụ:")
        print("  python pattern_commit.py preview HEART")
        print("  python pattern_commit.py create HEART 2025-01-05")
        sys.exit(0)
    
    action = sys.argv[1]
    
    if action == "preview":
        pattern_name = sys.argv[2] if len(sys.argv) > 2 else "HEART"
        preview_pattern(pattern_name)
        
    elif action == "create":
        if len(sys.argv) < 4:
            print("❌ Thiếu tham số!")
            print("   Cú pháp: python pattern_commit.py create <pattern> <start_date>")
            sys.exit(1)
        
        pattern_name = sys.argv[2]
        start_date = sys.argv[3]
        
        confirm = input(f"\nTạo pattern '{pattern_name}' từ ngày {start_date}? (y/n): ")
        if confirm.lower() == 'y':
            create_pattern(pattern_name, start_date)
        else:
            print("Đã hủy.")
