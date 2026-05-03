@echo off
echo.
echo ============================================
echo  Travel Deals - Production Build
echo ============================================
echo.

where hugo >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Hugo not found.
    echo Install: https://gohugo.io/installation/
    pause
    exit /b 1
)

echo [1/3] Removing old public folder...
if exist public rmdir /s /q public

echo [2/3] Building...
hugo --minify --gc

if errorlevel 1 (
    echo.
    echo [ERROR] Build failed.
    pause
    exit /b 1
)

echo [3/3] Done!
echo.
echo Output : %~dp0public\
echo.

for /f %%i in ('dir /s /b public\*.html 2^>nul ^| find /c ".html"') do echo Pages  : %%i

echo.
pause
