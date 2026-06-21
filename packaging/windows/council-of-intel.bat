@echo off
setlocal
cd /d "%~dp0"

set EXE=%~dp0council-of-intel.exe
if not exist "%EXE%" set EXE=%~dp0..\..\dist\council-of-intel\council-of-intel.exe
if not exist "%EXE%" set EXE=%~dp0..\dist\council-of-intel\council-of-intel.exe
if not exist "%EXE%" (
  echo No encuentro council-of-intel.exe.
  exit /b 1
)

echo [1] TUI
echo [2] Web
echo [3] Dry-run
set /p CHOICE="> "

if "%CHOICE%"=="1" "%EXE%" --tui
if "%CHOICE%"=="2" "%EXE%" --web
if "%CHOICE%"=="3" "%EXE%" --dry-run
if not "%CHOICE%"=="1" if not "%CHOICE%"=="2" if not "%CHOICE%"=="3" echo Opcion invalida.

endlocal
