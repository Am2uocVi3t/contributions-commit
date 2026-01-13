@echo off
echo ========================================
echo GitHub Auto Commit System
echo ========================================
echo.
echo 1. Xem truoc commits (preview)
echo 2. Chay tao commits
echo 3. Xem truoc pattern
echo 4. Tao pattern commits
echo 5. Thoat
echo.
set /p choice="Chon (1-5): "

if "%choice%"=="1" (
    python auto_commit.py preview
) else if "%choice%"=="2" (
    python auto_commit.py
) else if "%choice%"=="3" (
    set /p pattern="Nhap ten pattern (LOVE, HI, HEART, CODE): "
    python pattern_commit.py preview %pattern%
) else if "%choice%"=="4" (
    set /p pattern="Nhap ten pattern: "
    set /p start_date="Nhap ngay bat dau (YYYY-MM-DD): "
    python pattern_commit.py create %pattern% %start_date%
) else if "%choice%"=="5" (
    exit
)

pause
