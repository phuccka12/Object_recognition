@echo off
echo ========================================
echo   Creating Backup Before Git Pull
echo ========================================

set backup_folder=backup_%date:~-4%%date:~3,2%%date:~0,2%_%time:~0,2%%time:~3,2%
set backup_folder=%backup_folder: =0%

echo Creating backup in: %backup_folder%
mkdir %backup_folder%

echo Copying files...
xcopy *.py %backup_folder%\ /Y
xcopy *.md %backup_folder%\ /Y
xcopy *.txt %backup_folder%\ /Y

echo Backup completed!
echo Safe to run: git pull origin main
pause
