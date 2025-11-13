@echo off
chcp 65001
title Auto IP Changer - Setup Builder

setlocal EnableDelayedExpansion

echo ========================================
echo    AUTO IP CHANGER - WINDOWS SETUP BUILDER
echo ========================================
echo.

:: Kiểm tra và tải NSIS nếu chưa có
set "NSIS_PATH=%ProgramFiles(x86)%\NSIS"
if not exist "%NSIS_PATH%\makensis.exe" (
    echo [INFO] Đang tải NSIS Compiler...
    powershell -Command "Invoke-WebRequest -Uri 'https://nsis.sourceforge.io/mediawiki/images/3/3c/NSIS_3.09_setup.exe' -OutFile 'nsis_setup.exe'"
    if exist "nsis_setup.exe" (
        echo [INFO] Đang cài đặt NSIS...
        start /wait nsis_setup.exe /S
        timeout /t 5
        del nsis_setup.exe
    ) else (
        echo [ERROR] Không thể tải NSIS!
        pause
        exit /b 1
    )
)

:: Tạo thư mục tạm
if not exist "temp_build" mkdir temp_build

:: Kiểm tra Python
echo [INFO] Kiểm tra Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo [INFO] Đang tải và cài đặt Python...
    powershell -Command "Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.11.9/python-3.11.9-amd64.exe' -OutFile 'python_installer.exe'"
    if exist "python_installer.exe" (
        echo [INFO] Đang cài đặt Python (có thể mất vài phút)...
        start /wait python_installer.exe /quiet InstallAllUsers=1 PrependPath=1 Include_test=0
        timeout /t 10
        del python_installer.exe
        
        :: Refresh PATH
        for /f "skip=2 tokens=1-2*" %%a in ('reg query "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Environment" /v Path 2^>nul') do (
            set "PATH=%%c"
        )
    ) else (
        echo [ERROR] Không thể tải Python!
        pause
        exit /b 1
    )
)

:: Cài đặt thư viện
echo [INFO] Đang cài đặt thư viện Python...
pip install --upgrade pip
pip install pyinstaller psutil tkinter

:: Tạo file requirements.txt
echo psutil==5.9.6 > requirements.txt

:: Đóng gói ứng dụng
echo [INFO] Đang đóng gói ứng dụng...
pyinstaller --onefile --windowed --name "AutoIPChanger" --icon=icon.ico --distpath temp_build ip_changer_windows.py

if errorlevel 1 (
    echo [ERROR] Đóng gói thất bại!
    pause
    exit /b 1
)

:: Tạo file uninstaller script
echo [INFO] Đang tạo uninstaller...
echo @echo off > "temp_build\uninstall.bat"
echo echo Đang gỡ cài đặt Auto IP Changer... >> "temp_build\uninstall.bat"
echo timeout /t 2 >> "temp_build\uninstall.bat"
echo rmdir /s /q "%%APPDATA%%\AutoIPChanger" >> "temp_build\uninstall.bat"
echo del "%%USERPROFILE%%\Desktop\AutoIPChanger.lnk" >> "temp_build\uninstall.bat"
echo echo Đã gỡ cài đặt thành công! >> "temp_build\uninstall.bat"
echo pause >> "temp_build\uninstall.bat"

:: Biên dịch setup với NSIS
echo [INFO] Đang tạo file setup.exe...
"%NSIS_PATH%\makensis" installer.nsi

if errorlevel 1 (
    echo [ERROR] Tạo setup thất bại!
    pause
    exit /b 1
)

:: Dọn dẹp
rmdir /s /q temp_build
rmdir /s /q build
del requirements.txt

echo.
echo ========================================
echo ✅ TẠO SETUP THÀNH CÔNG!
echo 📦 File cài đặt: AutoIPChanger_Setup.exe
echo ========================================
echo.
echo Nhấn phím bất kỳ để kết thúc...
pause >nul