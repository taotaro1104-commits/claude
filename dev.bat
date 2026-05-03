@echo off
echo.
echo ============================================
echo  Travel Deals - Dev Server
echo ============================================
echo.

where hugo >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Hugo not found.
    echo Install: https://gohugo.io/installation/
    pause
    exit /b 1
)

echo [1/2] Stopping any process on port 1313...
powershell -NoProfile -Command "$p = (Get-NetTCPConnection -LocalPort 1313 -ErrorAction SilentlyContinue).OwningProcess; if ($p) { Stop-Process -Id $p -Force -ErrorAction SilentlyContinue; Start-Sleep 1 }"

echo [2/2] Starting dev server...
echo.
hugo version
echo.
echo URL : http://localhost:1313/
echo Stop: Ctrl+C
echo.

hugo server --buildDrafts --disableFastRender --port 1313 --bind 127.0.0.1

pause
