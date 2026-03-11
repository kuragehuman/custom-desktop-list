@echo off

echo Cleaning old build...
rmdir /s /q build
rmdir /s /q dist

echo Building...

pyinstaller --onefile --noconsole --name "ListApp" main.py

echo.
echo Done!
pause