@echo off
echo.
echo ============================================
echo  Travel Deals - New Content
echo ============================================
echo.
echo Select category:
echo   1. flights
echo   2. hotels
echo   3. ferries
echo   4. cruises
echo   5. tips
echo.
set /p category="Number (1-5): "

if "%category%"=="1" set section=flights
if "%category%"=="2" set section=hotels
if "%category%"=="3" set section=ferries
if "%category%"=="4" set section=cruises
if "%category%"=="5" set section=tips

if "%section%"=="" (
    echo [ERROR] Invalid number.
    pause
    exit /b 1
)

echo.
set /p filename="File name (e.g. cheap-osaka-flights): "

if "%filename%"=="" (
    echo [ERROR] File name is required.
    pause
    exit /b 1
)

echo.
echo Creating content\%section%\%filename%.md ...
hugo new content %section%/%filename%.md

if errorlevel 1 (
    echo [ERROR] Failed to create file.
    pause
    exit /b 1
)

echo.
echo [OK] content\%section%\%filename%.md created.
echo.
set /p openfile="Open in Notepad? (y/n): "
if /i "%openfile%"=="y" notepad content\%section%\%filename%.md

pause
