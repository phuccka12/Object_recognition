@echo off
echo ========================================
echo   AI Object Detection Studio
echo   Auto Deploy to GitHub
echo ========================================
echo.

echo [1/4] Checking current status...
git status

echo [2/4] Adding all files...
git add .

echo [3/4] Committing changes...
set /p message="Enter commit message (or press Enter for default): "
if "%message%"=="" set message="Update AI Object Detection Studio"
git commit -m "%message%"

echo [4/4] Syncing with GitHub...
echo Pulling latest changes first...
git pull origin main

if errorlevel 1 (
    echo.
    echo ========================================
    echo   CONFLICT DETECTED!
    echo ========================================
    echo Please resolve conflicts manually:
    echo 1. Edit conflicted files
    echo 2. Run: git add .
    echo 3. Run: git commit -m "Resolve conflicts"
    echo 4. Run: git push origin main
    pause
    exit /b 1
)

echo Pushing to GitHub...
git push origin main

if errorlevel 1 (
    echo.
    echo Push failed! Try force push? (Y/N)
    set /p force="Force push (will overwrite remote): "
    if /i "%force%"=="Y" (
        git push origin main --force
        echo Force push completed!
    )
) else (
    echo.
    echo ========================================
    echo   SUCCESS! 
    echo   Repository updated on GitHub
    echo ========================================
)

pause
